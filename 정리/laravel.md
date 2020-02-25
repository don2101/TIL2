## Laravel

- PHP 7.x 이상 부터 지원되는 프레임 워크
- 기본적으로 MVC 패턴을 사용



### 1. laravel 설치

#### composer 설치 및 바로가기 설정

```
curl -sS https://getcomposer.org/installer | php
mv composer.phar /usr/bin/composer
```

- composer: PHP 의존성 관리 패키지. 프로젝트내에 라이브러리를 생성하고, 관리해주는 툴



#### zip-ext 설치

```
apt-get install -y zlib1g-dev && apt-get install -y libzip-dev
docker-php-ext-install zip
```



#### laravel 설치 및 laravel 환경변수 설정

```
composer global require laravel/installer
echo PATH=$PATH:~/.composer/vendor/bin/ >> ~/.bashrc
```



#### Mysql DB 연동

```
docker-php-ext-install pdo_mysql
```

- pdo_mysql 드라이버를 설치

```
composer require doctrine/dbal
```

- doctrine/dbal 설치: laravel에서 사용하는 db 연동 패키지



#### 프로젝트 생성

```
laravel new <프로젝트>
```



### 1. 구성 요소

#### Middleware

- Application으로 들어온 HTTP 요청을 간편하게 필터링하는 방법을 제공
  - ex) 사용자가 인증이 되었는지?, CORS 검증 등...
  - django의 미들웨어와 유사
- `app/Http/Middleware`에 위치



##### Before & After 미들웨어

- Application 시작 순서를 정한다
- 미들웨어가 HTTP 요청을 처리하기 전, 후로 나뉘어 작동



#### Artisan Console

- Artisan: 라라벨에 포함된 커맨드라인 인터페이스(CLI)
  - application 개발에 도움이 되는 명령어들을 제공

> 실행 가능 명령어 확인

```bash
php artisan list

# 명령어에 대한 도움말
php artisan help migrate
```



#### Service Container

- 클래스의 의존성을 관리하고 주입하는 도구
  - 의존성 주입: 프로그래밍에서 요소간 관계가 프로그래밍 내부가 아닌 외부 설정파일로 부터 정의됨



#### Service Provider

- 라라벨 어플리케이션의 부팅의 핵심
- 라라벨의 모든 코어 서비스는 서비스 프로바이더로 부터 부트스트래핑
  - 부트스트래핑(부팅): 서비스 컨테이너에 바인딩, 이벤트 리스너, 미들웨어, 라우팅 등 **구성요소를 등록**하는것
- `config/app.php` 에서 프로바이더 리스트를 확인할 수 있다
- 프로바이더는 **지연**된다: 모든 요청에 대해 로드 되는 것이 아닌 필요할 때에 로드된다.



#### Fasade

- application의 서비스 컨테이너에서 사용가능한 클래스들에 대한 정적 인터페이스 제공
- 서비스 컨테이너에 등록된 클래스들에 대한 정적 프록시 역할
- `Illuminate\Support\Facades`에 정의되어 있다.



### 2. 기능 관련

#### Logging

- 프로그램에서 발생하는 사건이나 알림등을 기록
- 라라벨에서 제공하는 로깅 모듈은 파일이나 DB로 저장 가능하고, 슬랙으로도 보낼 수 있다.
- ` config/logging.php ` 에서 로깅 관련 설정 가능
  - 채널을 설정하여 로깅 설정 가능



##### Channel

- 로그를 작성할 때 사용하는 채널
- 채널마다 로그 옵션을 적용할 수 있다.
- 기본으로 설정된 채널
  - stack: 다중 채널
  - single: 하나의 파일을 기반으로 하는 채널
  - daily, slack, syslog...

> 채널 설정 예시

```php
'daily' => [
    'driver' => 'daily',
    'path' => storage_path('logs/laravel.log'),
    'level' => 'debug',
    'days' => 14,
],
```



##### level

- 로그를 작성하는 8개의 레벨
- emergency, alert, critical, error, warning, notice, info, debug
- emergency의 레벨이 가장 높으며, 로그 레벨을 설정하면 **해당 레벨 이상**의 로그만 출력, 기록된다.





### Model 선언

1. Model을 생성
2. migration진행: table을 생성하는 명령어
3. $fillable 사용









