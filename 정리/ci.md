## CI 작동 방식

### 1. user가 url를 통해 요청

- a/b/ 를 요청한다.



### 2. Route

- 기본 패턴: `controller-class/controller-method/(args)`



### 3. Controller

- 기본적으로 CI의 모듈, 모델, 리소스를 로드하는 역할
- url의 첫번째 arg는 controller 내부의 해당되는 class에 mapping
  - controller내부의 a.php의 class a에 mapping
- 두번째 arg는 class a 내부의 b method에 mapping
- model을 이름으로 불러와 사용
  - model에서 정의한 메서드 사용하여 데이터 접근
- View를 호출



#### controller life cycle

- 기본적으로 method에 대한 call이 발생할 때 마다 instance 생성
- CI에서 영구적인 instance는 존재하지 않는다.
  - session manager를 사용하여 해당 session에 대해 영구적인 instance 저장 가능
  - cookie를 사용한 방법도 있다.



### 4. Model

- DB에 접근하여 로직을 처리
- query는 model 안에서 정의
- C.I 내부의 Query Builder(db 접근 계층)를 통해 DB 접속을 한다.
  - 다수의 query를 한번 생성하고,  DB와 연동
- model 내부에서 CRUD 관련 메서드를 모두 정의



### 5. View

- Controller로 부터 호출된 view를 rendering
- Controller에서 받은 데이터를 사용할 수 있다.



### 6. etc.

#### Helper

- 작업에 도움을 주는 라이브러리
- 객체지향적으로 작성되지 않으며, 절차적.
- 특정 한가지 일만 수행하고, 다른 헬퍼에 의존하지 않는다.
- 사용하고자 하는 클래스, 메서드에서 로드 후 사용
- 로드: 한번 로드하면 컨트롤러, 뷰 등에서 글로벌하게 사용
  - CI는 application/helpers 폴더를 먼저 살핀 후 system/helpers 폴더를 살핀다.
  - ex) url_helper.php 로딩: $this->load->('url')
- 로드 후 PHP 표준 함수 사용하듯이 사용



#### CI_library

- 보통 컨트롤러의 생성자에서 로드
- 클래스 내부 메서드에 library 기능을 작성
- 인스턴스화 해서 사용
- $this->load->library



`$this` 는 컨트롤러, 뷰, 모델에서만 사용

다른 모듈에서 CI의 클래스를 사용

`$CI =& get_instance();`



#### autoload

- CI에서 사용되는 패키지, 라이브러리, 드라이버, 헬퍼, 모델 등등에 대해 필요할 때 마다 로드해서 사용
- 그러나 session과 DB같이 전역적으로 쓰이는 것들은 매번 로드하기 귀찮을 수 있다
- autoload에서 각 항목의 요소를 자동 로드하여 편하게 사용



#### $this->load

- CI에서 사용되는 패키지, 라이브러리, 드라이버, 헬퍼, 모델을 로드해서 사용
- 보통 각 클래스에서 



$query->result => 해당하는 모든 결과를 2중 array로 반환

$query->row_reulst => 해당하는 결과 1개의 array로 반환



#### DB 재연결

- 대용량 처리 중 DB 연결 시간 초과가 날 가능성이 있다면, 다음 쿼리를 날리기 전에 reconnect() 함수를 사용





### index.php 작동 방식







### DB 연결 오류 해결 과정

#### 1. mysqli가 설치되지 않은 php image였다.

- 애초에 php.ini가 로드 되지도 않았다.
- extension_dir 설정도 제대로 안되어 있었다.

##### 해결

- extension_dir을 `phpinfo()`에서 확인하여 추가
- php.ini 위치도 `phpinfo()`에서 확인하고 해당 위치에 php.ini 추가



##### mysqli 설치

inside the docker container bash terminal

```php
# docker-php-ext-enable mysqli
```

if mysqli is not installed which you will come to know from the output of above command

```php
# docker-php-ext-install mysqli
```



#### 2. client측에서 알 수 없는 character를 server가 송신

- my.cnf에서 설정을 수정하여 해결



#### 3. mysql 인증 문제

- 8버전 이상부터 인증하는 방식이 변했다고 한다.
- mysql 내에서 들어오는 요청에 대한 인증 방식을 변경하여 해결





### docker php-apache 설정

1. mysqli 설치
   - (docker-php-ext-install mysqli)
2. php.ini-development 수정
   - Date수정 (Asia/Seoul)
   - extension_dir 수정
   - mysqli extension 추가
3. php.ini으로 파일명 변경

