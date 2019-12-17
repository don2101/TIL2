## Laravel Service Provider

- Laravel 어플리 케이션 부팅의 핵심
- 모든 코어서비스를 부팅(작동)시킨다.
  - 서비스 컨테이너에 바인딩, 이벤트 리스너, 미들웨어, 라우트 등을 등록
- `config/app.php`의 `providers` 배열에서 프로바이더를 관리



### Provider 작성, 등록

##### Provider 파일 생성

```bash
php artisan make:provider RiakServiceProvider
```

- 이후 `config/app.php` 파일에서 `providers` 배열 내에 프로바이더 등록



#### register method

- 프로바이더 작성시에 필요한 메서드
- 서비스 컨테이너에 객체를 바인딩 하는 작업을 수행
  - 바인딩하면 **자동으로** 서비스 컨테이너에 바인딩
- 이벤트 리스너, 라우트, 다른 기능을 **절대** 작성하지 말 것
  - 다른 서비스 프로바이더의 의존성이 로드되지 않았을 수 있다.

> 서비스 컨테이너에 객체를 바이딩

```php
public function register()
{
    $this->app->singleton(Connection::class, function ($app) {
        return new Connection(config('riak'));
    });
}
```

- 서비스 프로바이더 메서드 안에서 언제든지`$app` 속성을 사용할 수 있으며, 이를 통해 서비스 컨테이너에 접근
- `Connection:Class`: 클래스 path를 포함한 클래스 이름을 string으로 리턴



#### boot method

- 서비스 프로바이더 내에서 다른 의존성이 모두 설정된 다음 해야할 작업을 수행
- boot는 다른 서비스 프로바이더들이 모두 등록(`register`)된 이후에 호출되므로 다른 의존성을 모두 사용할 수 있다.

```php
public function boot()
{
    view()->composer('view', function () {
        //
    });
}
```

- 다른 의존성이 모두 등록된 후 `view composer` 등록



> 타입 힌트도 가능

```php
public function boot(ResponseFactory $response)
{
    $response->macro('caps', function ($value) {
        
    });
}
```

- `ResponseFactory`를 호출하여 자동으로 바인딩
- 바인딩할 객체를 인자로 넘기면 서비스 컨테이너가 자동으로 의존성 주입



#### 지연 로딩

- key만을 등록하여 나중에 바인딩이 필요한 경우에 바인딩 하고 결과를 리턴
- key를 등록해놓기만 하면 나중에 로딩을 할 때 실제 바인딩을 진행
- 정확하게 얘기하면 `register` 함수가 호출되는 시기를 늦춘다.

```php
<?php
namespace App\Providers;

use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;
use App\Models\MyConnection;
use Illuminate\Support\Facades\Log;

class TestProvider extends ServiceProvider implements DeferrableProvider
{

    public function register()
    {

        # instance를 사용한 직접 바인딩
        echo "instance binding\n";
        Log::info("instance binding");
        $api = new MyConnection();
        $this->app->instance(MyConnection::class, $api);
        
        # closure를 사용한 바인딩
        $this->app->bind(MyConnection::class, function($app) {
            echo "closure binding\n";
            Log::info("closure binding");
            return new MyConnection();
        });
    }

    public function provides() {
        echo "provides\n";
        Log::info("provides");
        return [MyConnection::class];
    }
}

```



>#### Closure 방식 vs instance 방식

- closure 방식은 **무조건 지연**된다
  - 해당 객체를 호출하여 사용할 때 객체 생성 및 바인딩이 발생
- instance 방식은 지연로딩 시에만 지연



> #### 정상적인 로딩 vs 지연 로딩

- 해당 **객체를 사용**할 때 지연 로딩이 발생
- 정상적인 로딩은 request가 들어온 이후 **bootstraping 단계**에서 실행



![정상](https://user-images.githubusercontent.com/19590371/70958989-37302a80-20be-11ea-894d-55d956f859c3.PNG)

- 정상적인 로딩 결과
- instance 바인딩을 먼저 실행한 후 호출이 들어왔을 때 closure 바인딩을 실행



![lazy](https://user-images.githubusercontent.com/19590371/70958990-37302a80-20be-11ea-90fd-36d864b2f3a9.PNG)

- 지연 로딩 결과
- provides 함수를 통해 먼저 객체를 등록
- 이후 호출이 들어오면 instance로딩과 closure 로딩을 진행



> #### complie?

- 프로바이더를 변경하더라도 미리 컴파일된 파일이 캐시되어 있다.
- 따라서 수정안을 적용하려면 `php artisan clear-compiled` 로 컴파일된 파일을 지우고 실행



