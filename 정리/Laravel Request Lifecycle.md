## Laravel Request Lifecycle

- Laravel Application에 요청이 들어왔을 때 작동하는 흐름을 이해한다.



### 1. index.php

- 요청이 들어오는 시작점
- 웹 서버를 통해 들어온 모든 요청은 `index.php`에게 전달된다.
- 요청을 직접 처리하는 로직 보다, **laravel에서 필요한 부분을 로딩**하는 시작점



#### Autoloader 로딩

```php
require __DIR__.'/../vendor/autoload.php';
```

- Composer는 자동으로 생성되는 **class loader**를 제공
  - Composer: PHP 라이브러리 의존성 관리에 대한 표준을 제공하는 PHP 패키기 관리자
    - 어플리케이션에서 필요한 의존성 설치
- 수동으로 class를 불러오는게 아닌 autoloader를 사용하여 필요한 class를 자동으로 불러온다.



#### Bootstraping

```php
$app = require_once __DIR__.'/../bootstrap/app.php';
```

- Laravel application을 가동(bootstrap)을 위한 설정
- 연결할 커널,  예외 처리 모듈을 불러온다.



### 2. HTTP / Console 커널

- `index.php` 를 거친 요청은 `HTTP 커널` 이나 `Console 커널` 중 하나로 보내진다.
- 커널을 통해서 request를 처리하고 response를 반환
- 서비스 프로바이더 로딩



#### HTTP 커널

- bootstrappers(시작 코드) 정의
- 요청이 처리되기 전 통과하는 미들웨어 목록을 정의











