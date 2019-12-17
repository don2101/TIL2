## Laravel Session

### 1. Session

- 사용자의 정보를 저장하는 공간
- **서버**에 저장되는 데이터
- **일정시간** 동안 같은 사용자로 부터 들어오는 요구를 하나의 요청으로 본다.
  - 일정시간: 유저가 브라우저를 통해 **접속한 시점** 부터 **연결을 끝내는** 시점
- 서비스를 이용하는 사용자의 정보를 저장하여 재방문시 사용자를 식별
- **저장된 데이터**로 **사용자를 식별**한다.



#### cache와 session의 차이?

- cache에는 만료 시간이 존재한다. session의 만료 시간은 session이 닫힐 때 까지다.
- session은 사용자를 기억하기 위해 사용자의 정보를 저장
  - 사용자 마다 저장되는 정보가 다르다
- cache는 자주 사용되는 로직을 저장하여 동일한 요청에 대해 더욱 빠르게 응답하기 위한 것
- 둘 다 자주 사용된다는 특성이 있고, 이를 저장해서 처리하기 위해 저장소가 필요한 것
- 결국 저장소를 어떤 걸 쓰느냐는 문제가 되지 않는다.
- 다만, 사용하는 상황, 환경에 따라 로직적으로 분리할 뿐



### 2. Laravel Session

- Laravel에서 세션 저장소에 대한 인터페이스를 제공
- 다양한 driver로 session에 관한 정보를 저장하고 불러올 수 있다.
- `config/session.php`에서 설정 가능



#### Session driver의 종류

- file, cookie, db, apc, memcache, redis, array등 사용 가능
  - file: 파일 디렉토리에 저장
  - cookie: 암호화된 쿠키를 사용하여 안전하게 저장
  - database: 세션을 관계형 db에 저장
  - memcached / redis: 캐시를 기반으로 빠르게 저장
  - array: php배열에 저장하며 데이터와 세션이 지속되지 않는다



### 3. 세션 사용하기

#### Global Session Helper

- 글로벌 `session()` 함수를 통해 세션에서 데이터를 찾거나 저장하는 경우에 사용
- `key` - `value` 형태로 데이터를 저장하며, 데이터가 있을 경우 해당 데이터에 접근

```php
$value = session('key');
```



#### Request Instance

- 함수에서 요청으로 들어온 `Request` 객체를 통해 session에 접근
- 서비스 컨테이너에 의해 자동으로 의존성이 주입된다.
- 마찬가지로 `key` - `value` 형태로 데이터 저장, 접근



#### 두 방법이 존재하는 이유

- Laravel은 하나의 기능을 수행하기 위해 하나의 방법만을 제공하지 않는다.
- Laravel의 철학인 깔끔하고, 쉽고, 직관적인 코드를 위해 **하나의 기능에 대한 여러 인터페이스**를 두는 것
- 성능상의 차의는 거의 없으며, 상황에 따라 기능을 맞춰 쓴다.



#### 데이터 임시 저장

- 다음번의 요청에만 사용하기 위한 세션 아이템 저장 방법
- `flash` 메서드를 사용하여 데이터 저장
- 다음에 이어지는 HTTP 요청에만 사용되고 이후에는 아이템 삭제



### 3. 세션 설정

#### Lifetime, expire_on_close

- 세션 아이템이 저장되는 기간을 분단위로 설정
- 해당 기간이 지나거나 `expire_on_close` 가 설정되고 창을 닫으면 세션 데이터를 삭제
- 사용자에게 일정 시간의 사용시간을 부여하는데 사용



#### Encryption

- 세션 데이터가 저장되기 전 데이터를 암호화하여 저장
- Laravel secret key와 함께 암호화



### 4. File을 사용한 Session 관리

- `framework/sessions/` 에 저장
- 파일 제목은 암호화 하여 저장



##### 파일 저장

![file](https://user-images.githubusercontent.com/19590371/70487068-73501200-1b37-11ea-9633-40c1fc13c9a9.PNG)



### 5. Database를 사용한 Session 관리

##### session data 저장용 table 생성

```bash
php artisan session:table # table 생성 용 migration 생성
php artisan migrate
```



#### 저장하는 데이터 id를 정하는 방법

- 저장하려는 데이터가 이미 있다면, 같은 레코드를 더이상 만들지 않는다.
- 데이터 내용을 hash나 암호화 하여 이미 같은 id가 있다면 추가 저장을 하지 않는다.



### 6. Redis를 사용한 Session 관리



### 7. Memcached 사용한 Session 관리







