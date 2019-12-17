## Logging

- 어플리케이션이 어떤 일을 하는지, 어떤 사건이 발생했는지를 기록
- 최대한 자세히 기록할 수록 좋으며, 시스템 관리등에 도움이 된다.



### 1. Monolog

- PHP 로깅 라이브러리
- Laravel에서는 로그 핸들링을 위해 Monolog를 사용



### 2. 설정

- `config/logging.php` 에서 로그 관련 설정 가능



#### Channel

- 로깅 관련한 드라이버, 저장소, 레벨 등의 설정을 묶어놓은 단위
- 로깅 채널을 로드하여 로깅을 진행
- 하나의 채널에서 여러개의 채널을 불러와 사용도 가능



#### Stack

- 여러개의 채널을 하나로 묶어서 사용하는 채널
- 동일 채널을 여러번 설정하면 여러번 로깅



#### Level

- 로그를 기록하는 레벨을 설정
- 해당 레벨 이상의 로그만 기록하며, 상황에 따라 레벨을 정해서 사용한다.
- level: **emergency**, **alert**, **critical**, **error**, **warning**, **notice**, **info**, **debug**
  - 왼쪽일수록 상위 레벨



### 3. Logging 하는 방법

#### 어떻게 찍는가

- 개발, 배포 등 상황에 따라, 시기에 따라 모두 다르다. 상황에 맞게 구성을 하고, formatting을 하는 것이 중요.
- 주로 날짜, 기능 등으로 나누며, 각 서버에서 기록된 분산된 로그들을 **하나의 로그 서버에서 수집**하여 에러나 장애를 찾는데 사용
- Laravel에서는 **이벤트** 기능을 사용하거나, 모델관련 연산의 경우 **옵저버 객체**를 통해 연산을 시작하거나 끝내면 로그를 기록
- 혹은 프로바이더를 통해 특정 컨트롤러에 일괄적으로 로그를 남기는 경우도 있다.



#### 성능

- 로깅을 하면 기록과 분석에 사용할 정보가 남지만, 너무 많이 기록하면 I/O 횟수 등 리소스가 많이 소모되기 때문에 기록과 성능 사이에서 적절하게 사용
- 보통 개발할때는 `Debug` 까지 찍어 로그를 확인하고, 배포 이후로는 `Debug` 보다 높게 레벨을 설정하여 어느정도 성능을 확보하는 것이 중요하다.



#### Formatting

- 로깅을 할 때 어떤 정보를 기록하는지 또한 중요
- Laravel logging에서는 `message` 이후에 배열로 추가 정보를 받아서 기록한다.



##### 예시

```php
/*
@method static void info(string $message, array $context = []) # 메서드 명세
*/  

Log::info("Person 객체 출력", ["className" => static::class]);
```



##### 출력

![class](https://user-images.githubusercontent.com/19590371/70602266-569b0380-1c37-11ea-8dd7-9a8dbf263894.PNG)



### 4. Single Logging Channel

- 파일을 기반으로 로그를 저장
- 하나의 파일에 log를 이어서 기록



> 로그 파일을 확인하는데 한글이 깨진다

- vim을 통해 로그 파일을 확인하면 인코딩이 정의가 되어 있지 않아서 한글이 깨지는 현상이 발생할 수 있다.

```bash
set encoding=utf-8
set fileencodings=utf-8,cp949
```

- encoding과 file encoding을 정의하면 정상적으로 한글을 출력할 수 있다.



##### 로그 기록

```php
public function setPerson(Request $request) {
    if ($request->isMethod('get')) {
        Log::info("person 입력 페이지 진입");

        return view('input');
    } else {
        $data = $request->all();
        $person = new Person();
        $person->name = $data['name'];
        Log::info("Name 입력: ".$data['name']);

        $person->save();
        Log::debug("Person 객체 저장");

        return redirect('/getPerson');
    }
}
```



##### 로그 확인

![logging](https://user-images.githubusercontent.com/19590371/70581701-71e81d80-1bfb-11ea-86bb-473ed300b4ea.PNG)





### 5. Daily Logging Channel

- 일 단위로 로그파일을 구분하여 기록
- `single logging channel` 과 동일한 디렉토리에 생성되지만 파일명 뒤에 날짜를 붙여 구분
- 일 단위 파일은 이어서 로깅



#### Options

- `single channel` 과 `daily channel`은 세 가지 옵션 설정을 갖고있다.



##### bubble

- 로깅을 처리한 후 다른 채널로 버블링 되는지 설정
- 해당 채널에서 로그를 기록하고 stack에서 정의된 다음 채널에도 기록하는지 정의



##### permission

- 로그파일 사용 권한을 설정
- string 형태로 지정(ex "755")
- 이미 생성된 파일의 권한도 변경



##### locking

- 기록하기 전 로그 파일을 lock한 후 기록



### 6. Papertrail

- 시스템이 거대해지면 쌓이는 로그가 많아지고, 로그에서 정보를 얻는 것이 어려워진다.
- 빠르게 장애감지를 하고, 원하는 정보를 로그로부터 얻기 위해 분산된 서버들의 로그를 **집중화** 해야 한다.
- host와 port를 기반으로 원격 서버에 로그를 저장하는 유료 서비스
- 로그 자동 삭제, 보존, 보존 기간 등을 설정하여 사용



#### 설치

1. PHP sockets 설치 및 적용
2. Papertrail 가입 후 url과 port 생성
3. `.env` 에 Papertrail용 url과 port 적용



#### 특징

- 분산 환경에서도 로그를 통합적으로 관리할 수 있어 편리
- 뛰어난 검색 기능
- 로그 백업, 보존, 삭제, 제한 용량 등 설정을 편하게 가능





### 7. Syslog

- 표준 메세지 로깅 프로그램
- 프로그램이나 시스템이 생성하는 메세지를 저장하고, 로그 메세지를 제공
- Laravel에서 사용하면 파일에 직접 로그를 저장하는 것이 아니라 `rsyslog` 등의 프로그램을 통해 시스템에 로깅을 하도록 요청
- `logger log <메세지>`: bash에서 명령어으로 syslog에 기록 가능



#### 제공하는 정보

- 시스템 관리
- 보안 알림
- 정보 분석, 디버깅, 메세지 등을 제공



#### 사용하는 이유

- 시스템에 로깅을 위임하면 시**스템에서 제공**하는 **네트워크나 기본 기능**들을 로깅에 적용할 수 있다.
- 이러한 기능을 통해 로그 내용을 다른 서버나 DB로 전송하거나 하나의 서버에서 수합하는 것이 가능하다.
- 또한, 로깅 관련 기능을 어플리케이션과 분리하여 **종속성을 줄이고**, **확장성을 늘린다**.
- 시스템을 로깅을 위한 하나의 **인터페이스로** 생각



> syslog의 인터페이스 역할

![syslog](https://user-images.githubusercontent.com/19590371/70607057-1ccefa80-1c41-11ea-8a7f-368cd28e1615.png)



#### 특징

- 표준이기 때문에 운영체제에 상관 없이 사용 가능
- 다양한 설정이 가능하며 원격으로 로그를 전송하여 파일이나 DB에 기록하는 것도 가능
  - Papertrail에 기록할 때 이러한 구조를 사용
- 각종 패키지를 받아 추가 모듈로 적용할 수도 있다



#### Facility

- 메세지를 발생시킨 프로그램의 타입
- 프로그램 종류: auth, authpriv, daemon, cron, ftp, lpr, kern, mail, news, syslog, user, uucp ...



#### Serverity

- 메세지의 성격 또는 중요도
- 등급:  Emergency, Alert, Critical, Error, Warning, Notice, Info, Debug 
- Facility와 Serverity에 따라 메세지를 어느 파일에 기록할지 누구에게 알릴지를 결정한다.



#### Logrotate

- 로그가 너무 많이 쌓이면 관리가 힘들어지고 로딩 시간이 길어진다.
- 일정시간 단위로 로그를 삭제하거나 구분하여 저장하도록 도와주는 설정파일
- `/etc/logrotate.d`와 `/etc/logrotate.conf` 설정파일에서 관련 기능 설정



##### 로그 기록

![syslog](https://user-images.githubusercontent.com/19590371/70607408-bbf3f200-1c41-11ea-92ef-996163039c4f.PNG)

- 로깅을 요청하는 객체, 시간, 내용등을 기록
- `logger` 명령어를 통한 로그는 계정(로깅 주체)을 기록



### 8. Stderr

- 표준 에러를 사용해 로그를 기록하는 방식
- 콘솔에 로그를 남기는 목적으로 사용



> ### Standard Stream과 PHP

- 일반적인 프로세스는 I/O를 위해 표준 입력 스트림(Stdin stream), 표준 출력 스트림(Stdout stream), 표준 에러 스트림(Stderr stream)을 제어한다.
- Stdout과 Stderr를 둘 다 출력하는 관점에서는 같지만, Stderr는 버퍼를 사용하지 않고 바로 출력한다.
- 따라서 어떠한 상황에서도 에러를 출력할 수 있다.



#### PHP에서 표준 입출력 사용

```php
<?php
    $stdin = fopen('php://stdin', 'r');
    $line = fgets($stdin);
    $stdout = fopen('php://stdout', 'w');
    $out = fwrite($stdout, $line);
    $stderr = fopen('php://stderr', 'w');
    $err = fwrite($stderr, $line);
?>
```

- `fgets`로 사용자에게 커맨드 라인으로 입력을 받아 `fwrite`를 통해 커맨드 라인에 출력
- `php` 명령어로 실행





