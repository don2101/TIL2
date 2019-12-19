## Laravel Facade

- 서비스 컨테이너에 등록된 클래스들에 대한 **정적 인터페이스 제공**
  - 정적 프록시 역할
- Laravel에서 대부분의 Laravel 기능에 접근하는 많은 파사드를 제공
- Laravel에서 구현된 클래스, 메서드에 대한 인터페이스



#### 사용하는 이유

- 메서드를 직접 사용하는 것 보다 간결한 문법
- 의존성이 주입이 해결된 메서드 사용
- 테스트가 용이하다
  - 메서드에 대해 mock이나 stub를 생성할 수 있다.
- 코드의 유연성 제공
- Laravel에서 제공하는, 그리고 Container를 통해 등록한 메서드들을 손쉽게 사용하기 위함



### 1. 실제 구현

> ##### MyConnection.php

```php
<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class MyConnection extends Model {
    
    function __construct() {
        echo "Connection construct\n";
    }

    function run() {
        echo "run\n";
    }
}
```

- 사용할 객체 구현



> ##### TestProvider.php

```php
<?php
namespace App\Providers;

use Illuminate\Contracts\Support\DeferrableProvider;
use Illuminate\Support\ServiceProvider;
use App\Models\MyConnection;

class TestProvider extends ServiceProvider implements DeferrableProvider
{

    public function register()
    {
        $this->app->singleton('test', function ($app) {
            return new MyConnection($app);
        });
    }

    public function provides() {
        return ['test'];
    }
}

```

- Provider를 통해 구현 객체 mapping



> ##### Test.php에서 Facade 구현

```php
<?php
namespace Illuminate\Support\Facades;

class Test extends Facade
{

    protected static function getFacadeAccessor()
    {
        return 'test';
    }
}

```

- container에서 `test`라는 이름으로 mapping된 객체를 return



> ##### ProvideController.php

```php
<?php
namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

use Illuminate\Support\Facades\Test;

class ProvideController extends Controller {
    public function get(Request $request) {
        echo "call\n";
        Test::run();
    }
}

?>
```

- Controller에서 사용



### 2. 작동 흐름

![Laravel Facade](https://user-images.githubusercontent.com/19590371/70979282-bc363680-20f4-11ea-9899-86ddfe8d4d37.png)

- `Cache Facade`는 `Cache Factory`나 `Cache Contract`에서 구현한 메서드에 접근할 수 있는 프록시 역할



### 3. 파사드 vs 의존성 주입

#### 의존성 주입

- 클래스의 구현체를 변경할 수 있다.
- 테스트 과정에서 mock과 stub를 주입하여 테스트를 할 수 있다.



#### 파사드

- 정적 클래스 메서드는 mock과 stub로 대체하여 테스트 할 수 없다.
- 파사드는 컨테이너에 의해 의존성이 해결된 클래스 객체의 프록시 메서드로, 다이나믹 메서드를 사용하기 때문에, 주입된 클래스 인스턴스를 테스트 하는 것 처럼 테스트할 수 있다.



#### Test에서 사용

```php
class ProviderTest extends TestCase
{

    public function testBasicTest()
    {
        Cache::shouldReceive('get') // get에 대한 Mock 객체 반환
            ->with('key')
            ->andReturn('value');

    }
}
```





### 4. 실시간 파사드

- 어플리케이션의 모든 클래스를 파사드처럼 취급하는 기능



#### 사용 방법

```php
<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Log;
use App\Person;

class MyConnection extends Model {

    function personRun(Person $person) {;
        log::info($person->say());
        Log::info("person run");
    }
}
```

- 모델 `MyConnection`에서  `Person` 인스턴스를 주입받아 사용
- 주입된 `Person` 객체는 mock객체로 대체할 수 있다.
- 하지만 `personRun`을 호출할 때 마다 매번 주입하는것 보다 명시적으로 mock객체를 통해 테스트를 진행



```php
<?php
namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Log;
use Facades\App\Person;

class MyConnection extends Model {
    function personRun() {
        log::info(Person::say());
        Log::info("person run");
    }
}
```

- 주입하는 객체 루트 앞에 `Facades`를 붙이면 실행 단계에서 자동으로 `Person`에 대한 Facade 객체 생성
- 생성된 Facade 객체를 통해 메서드에 접근 가능











> ### 테스트 과정에서 발생한 문제

```php
# FacadeTest.php
use PHPUnit\Framework\TestCase;
use App\Models\MyConnection;

<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use App\Models\MyConnection;

class FacadeTest extends TestCase
{

    public function testExample()
    {
        $myConnection = new MyConnection();
        $myConnection->run();
        
        $this->assertTrue(true);
    }
}
```

- `MyConnection` 객체를 생성하여 테스트를 진행하는 상황



```php
# MyConnection.php
use Illuminate\Support\Facades\Log;

class MyConnection extends Model {
    
    function __construct() {
        echo "Connection construct\n";
        Log::info("Connection construct");
    }

}
```

- `MyConnection` 객체는 `Log` Facade를 사용



**phpunit으로 테스트를 돌려 봤으나 에러 발생**

![error](https://user-images.githubusercontent.com/19590371/71058510-6cfb0f00-21a3-11ea-8d66-c6e9fb74276a.PNG)

- MyConnection에서 사용하는 `Log` Facade에 대한 의존성이 주입되지 않아 에러 발생



#### 해결 방법

- `PHPUnit`에 있는 TestCase가 아닌 Laravel에서 제공하는 TestCase를 상속받아 테스트 구현
  - Laravel에서 제공하는 TestCase를 통해 testing 과정에서 필요한 의존성을 주입

```php
# use PHPUnit\Framework\TestCase;
use Tests\TestCase;
```



- 혹은, Facade에서 기본적으로 제공하는 mocking 기능을 사용하여 테스트 구현

```php
Cache::shouldReceive('get') 
                ->with('key')
```



