# Request Lifecycle
Laravel Framework에서 HTTP Request를 처리하는 과정의 개략적인 흐름

## 1. Request 진입
* 웹 서버(apache / nginx)의 설정에 의해 HTTP request가 Laravel의 `public/index.php` 파일로 전달
* Composer에 의해 생성된 autoloader definition 로드 (namespace, class...)
* `bootstrap/app.php`에 정의된 Laravel application의 instance **(Service Container)** 를 생성
    ~~~
    /* public/index.php */    

    <?php
    define('LARAVEL_START', microtime(true));
    
    /* Loads the Composer generated autoloader definition */
    require __DIR__.'/../vendor/autoload.php';  
   
    /* Create an instance of the application / service container */
    $app = require_once __DIR__.'/../bootstrap/app.php';
    
    ...
    ~~~

## 2. HTTP / Console Kernel
* HTTP Request는 HTTP Kernel에 의해 처리
    * Request의 종류에 따라 Console Kernel인지 HTTP Kernel인지가 결정
* HTTP Kernel은 `app/Http/Kernel.php`에 정의
    * `Illuminate\Contracts\Http\Kernel::class`에 bind된 Singleton Service Container
    
    ~~~
    <?php
    /* bootstrap/app.php */
    
    $app = new Illuminate\Foundation\Application(
        $_ENV['APP_BASE_PATH'] ?? dirname(__DIR__)
    );
    
    /* Bind important interfaces including HTTP / console kernel */
    $app->singleton(
        Illuminate\Contracts\Http\Kernel::class,
        App\Http\Kernel::class
    );
    
    $app->singleton(
        Illuminate\Contracts\Console\Kernel::class,
        App\Console\Kernel::class
    );
    
    $app->singleton(
        Illuminate\Contracts\Debug\ExceptionHandler::class,
        App\Exceptions\Handler::class
    );
    
    /* Returns the application instance. */
    return $app;
    ~~~
    
* HTTP Kernel은 `Illuminate/Foundation/Http/Kernel`을 상속
    * Request가 처리되기 전에 수행되는 bootstrapper 클래스들이 **bootstrappers** 배열에 정의 -> **bootstrap** 메소드 실행
    
        ~~~
        /* Illuminate/Foundation/Http/Kernel.php */
        
        class Kernel implements KernelContract
        {  
            /* The bootstrap classes for the application. */
            protected $bootstrappers = [
                'Illuminate\Foundation\Bootstrap\DetectEnvironment',    // detect the application environment
                'Illuminate\Foundation\Bootstrap\LoadConfiguration',
                'Illuminate\Foundation\Bootstrap\ConfigureLogging',     // configure logging
                'Illuminate\Foundation\Bootstrap\HandleExceptions',     // configure error handling
                'Illuminate\Foundation\Bootstrap\RegisterFacades',  
                'Illuminate\Foundation\Bootstrap\RegisterProviders',
                'Illuminate\Foundation\Bootstrap\BootProviders',
            ];
            ...
            /* Bootstrap the application for HTTP requests. */
            public function bootstrap()
            {
                if (! $this->app->hasBeenBootstrapped()) {
                    $this->app->bootstrapWith($this->bootstrappers());
                }
            }
            ---
        }
        ~~~
        ~~~
        /* Illuminate/Foundation/Bootstrap/RegisterProviders.php */
        
        <?php
        namespace Illuminate\Foundation\Bootstrap;
        use Illuminate\Contracts\Foundation\Application;
        
        class RegisterProviders
        {
            /* Bootstrap the given application. */
            public function bootstrap(Application $app)
            {
                $app->registerConfiguredProviders();
            }
        }
        ~~~
    * Kernel bootstrapping에 **Service Provider**들을 로딩하는 과정도 포함
        * `config/app.php`에 포함된 **providers** 배열에 정의
        * 각 Provider의 모든 **register** 메소드 수행 -> 모든 **boot** 메소드 수행
        
    * middleware 리스트 정의
        * HTTP session 작성 및 읽기, maintenance mode 여부 확인, CSRF token 처리...
        
        ~~~
        /* app/Http/Kernel.php */
        
        namespace App\Http;
        use Illuminate\Foundation\Http\Kernel as HttpKernel;
        
        class Kernel extends HttpKernel
        {
            /*
             * The application's global HTTP middleware stack.
             * These middleware are run during every request to your application.
             */
            protected $middleware = [
                \App\Http\Middleware\TrustProxies::class,
                \App\Http\Middleware\CheckForMaintenanceMode::class,
                \Illuminate\Foundation\Http\Middleware\ValidatePostSize::class,
                \App\Http\Middleware\TrimStrings::class,
                \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
            ];
            ...
        }
        ~~~
* HTTP Kernel의 **handle** 메소드 -> 전달된 Request에 대해 Response를 생성
* bootstrap 과정 및 Service Provider 등록이 완료되면 Request는 Router에 의해 특정 route 또는 controller로 전달
    * 전달되는 route에 따라 route specific middleware 실행
    
    ~~~
    /* public/index.php */    

    ...
    /* Handle the incoming request through the kernel, and send the associated response back. */
    
    $kernel = $app->make(Illuminate\Contracts\Http\Kernel::class);
    
    $response = $kernel->handle(
        $request = Illuminate\Http\Request::capture()
    );
    
    $response->send();
    
    $kernel->terminate($request, $response);
    ~~~
    ~~~
    /* Illuminate/Foundation/Http/Kernel.php */
        
    class Kernel implements KernelContract
    {  
        ...
        /* Handle an incoming HTTP request. */
        public function handle($request)
        {
            try {
                $request->enableHttpMethodParameterOverride();
                $response = $this->sendRequestThroughRouter($request);
            } catch (Exception $e) {
                $this->reportException($e);
                $response = $this->renderException($request, $e);
            } catch (Throwable $e) {
                $e = new FatalThrowableError($e);
                $this->reportException($e);
                $response = $this->renderException($request, $e);
            }
            
            $this->app['events']->fire('kernel.handled', [$request, $response]);
            
            return $response;
        }
        
        /* Send the given request through the middleware / router. */
        protected function sendRequestThroughRouter($request)
        {
            $this->app->instance('request', $request);
            
            Facade::clearResolvedInstance('request');
            
            $this->bootstrap(); // Bootstrapping
            
            return (new Pipeline($this->app))
                        ->send($request)
                        ->through($this->app->shouldSkipMiddleware() ? [] : $this->middleware)
                        ->then($this->dispatchToRouter());
        }
        ...
    }
    ~~~

## 3. 요약
1) HTTP Request에 의해 `public/index.php` 실행
2) Laravel application instance 생성(`bootstrap/app.php`)
3) application 생성 시 HTTP Kernel을 bind
4) Kernel 생성(make), Kernel내에 middleware 리스트 등록
5) Request를 parameter로 Kernel의 handle 메소드 수행
6) Request 처리 전 bootstrapping 수행
7) Request를 router로 전달, route 또는 controller로 전달하여 처리 수행
8) handle이 Response를 반환, Kernel 제거
