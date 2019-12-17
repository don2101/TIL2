## Laravel Cache

### 1. Cache

- 사용자가 자주 요구하는 데이터나 많은 시간이나 필요한 작업 결과를 미리 저장해 두는 것
- 결과를 미리 저장하여 다음 요구시에 더욱 빨리 응답할 수 있다



#### 단점

- 메모리나 디스크에 비해 접근 속도는 빠르지만 용량은 더욱 적다.
- 따라서, 모든 정보를 저장할 수 없으며, 정말 자주 사용되는 시간이 오래 걸리는 정보를 캐싱한다.



### 2. Laravel Cache

- 작업 결과를 캐시하기 위해 추가적인 저장 공간이 필요하다
- Laravel은 storage 패턴에 따라 저장 공간이 바뀌어도 저장 기능을 사용하는데 무리가 없도록 다양한 저장소에 대해 인터페이스를 제공한다.
- 저장소는 여러개를 선택할 수 있으며 각각의 저장 공간이 존재한다.
- `config/cache.php` 에서 캐시 관련 설정 가능



#### Cache Driver의 종류

- apc, array, database, file,  memcached, redis, dynamodb



### 3. file을 사용한 캐싱

- 파일을 저장소로 사용하는 방법
- 파일을 생성하여 캐시 정보를 저장하고 불러온다.
- 파일 저장 디렉토리를 따로 명시할 수 있으며, 해당 디렉토리에 캐시 정보를 저장
- 파일 저장이기 때문에 캐시를 하지 않는 것 보다 속도차이가 거의 나지 않는다.



#### 폴더/파일 명을 정하는 방법

- 기본적으로 `storage/framework/cache/data` 하부 디렉토리에 캐시 정보를 저장
- 저장하는 디렉토리와 파일명은 `key` 값을 SHA 1 방식으로 해싱하여 결정



> 35개의 레코드를 저장하는 file caching

```php
public function getCache(Request $request) {
    $persons = Cache::remember('persons', 1000, function() {
        return Person::all()->where('id', '<=', 35);
    });

    return response()->json($persons);
}
```



> 저장 결과

![cachedirc](https://user-images.githubusercontent.com/19590371/70203954-17197680-1762-11ea-917b-50b16b2e4271.PNG)

- `12/33/` 디렉토리에 캐시한 결과값 저장
- 해당 디렉토리 명은 `key` 값을 해시한 값



> cache 결과 삭제

```php
Cache::forget('persons');
```

- 캐시한 결과를 삭제하면 해당 디렉토리 내에 있는 결과를 삭제



### 4. memcached를 사용한 캐싱

- 메모리를 캐시 저장소로 사용하는 방법
-  memcached: 메모리를 사용해 캐시 서비스 제공하는 데몬
- 분산 메모리 캐싱으로 `key`-`value` 값으로 데이터를 저장
- 필요량 보다 많은 메모리가 필요하면 자동으로 시스템으로 부터 메모리를 사용한다.



#### 특징

- memory에 접근하여 데이터를 저장하기 때문에 file 방법 보다 속도가 빠르다.
- memory에 데이터를 저장하기 때문에 서버를 닫았다 열면 데이터가 모두 유실된다.



#### 설치

> 1. libmemcached 설치

```bash
apt-get install -y libmemcached-dev
```



> 2. php-memcached 설치

```bash
git clone https://github.com/php-memcached-dev/php-memcached.git
```

- php 전용 memcached 모듈
- 빌드 후 모듈을 `php.ini`에 등록



> 3. composer 사용하여 memcached 모듈 설치

```bash
composer require ext-memcached
```

- laravel에서 memcached를 사용하기 위한 추가 모듈



> 4. memcached 서비스 실행 / 종료

```bash
service memcached start
service memcached stop
```



##### memcached 관련 configurate, log

- 설정파일 위치: `/etc/memcached.conf`
- IP, Port, cache사용 용량 등을 설정할 수 있다.
- 로그파일 위치: `/var/log/memcached.log`



#### laravel에 caching 적용

- name 컬럼만을 갖고 있는 모델에 seed 데이터 삽입

```php
public function run()
{
    foreach(range(1, 3000) as $index) {
        Person::create([
            'name' => "testing"
        ]);
    } 
}
```



- seed 데이터 삽입 후 캐시를 사용한 것과 사용하지 않는 결과를 비교

```php
class CacheController extends Controller {
    public function getPerson(Request $request) {
        $persons = Person::all()->where('id', '<=', 3000);

        return response()->json($persons);
    }

    public function getCache(Request $request) {
        $persons = Cache::remember('persons', 1000, function() {
            return Person::all()->where('id', '<=', 3000);
        });
        
        return response()->json($persons);
    }
}
```



> Postman으로 데이터를 fetch한 결과

##### cache를 한 경우

![cache](https://user-images.githubusercontent.com/19590371/70203312-c6a11980-175f-11ea-9411-e322b4c4dec0.PNG)



##### cache를 하지 않은 경우

![nocache](https://user-images.githubusercontent.com/19590371/70203313-c7d24680-175f-11ea-9177-7a887c40da52.PNG)

- 둘의 결과에서 3000개의 결과를 가져오는데 300ms 정도의 차이가 나는 것을 볼 수 있다.



### 5. array를 사용한 캐싱

- php의 array에 캐시 결과를 저장하는 방법
- php가 구동되는 메모리에 저장



#### 특징

- 휘발성 데이터로 php가 종료되면 값이 소멸된다.
- 추가적인 저장소가 없어도 사용이 가능하다.
- 속도는 파일 캐싱보다 조금 느리다.



#### 예비 cache 저장소로 사용

- 추가적인 저장소를 필요로 하지 않는다.
- 저장소가 사용되지 못하는 상황에 대비하여 **예비 캐시 저장소**로 활용

```php
if ($this->cacheEnabled) {
    return cache->store('memcached')->remember("key", 10, callback());
} else {
    return cache->store('array')->rememberForever("key", callback());
}
```



### 6. DB를 활용한 캐싱

- DB를 캐시 저장소로 사용하는 방법



#### 특징

- DB에 접근해야 되기 때문에 속도는 가장 느리다
- DB에 캐시되어 있는 데이터를 추출하기 때문에 직접 DB에 데이터가 쌓이는 것은 아니다.
- 캐시 백업 용도로 사용 가능



#### table 생성

- DB를 사용하기 때문에 데이터를 저장할 추가 table 생성해야 한다.
- `connection` 설정에서 기본적으로 연결된 DB driver를 추가
- 기본 테이블 생성 후 사용

```bash
php artisan cache:table
```



### 7. Redis를 사용한 캐싱

#### Redis

- in-memory 데이터 저장 장소
- 오픈소스이며 DB cache, message broker 등으로도 쓰인다.
- `key` - `value` 형태로 자료를 저장하며, String, hash, list, set 등 다양한 자료구조 지원



#### Snapshot

- 특정 시점의 데이터를 디스크에 옮겨담는 방식
- 따라서, 서버를 껏다 켜도 디스크에 있던 데이터를 읽어 데이터가 유실되지 않는다.
- blocking, non-blocking 방식과, `aof`파일, database에 저장하는 방식이 있다.



#### AOF

- Redis의 모든 write/update 연산을 log파일에 기록하는 방식
- 서버를 재시작하면 write/update를 순차적으로 실행하여 데이터를 복구
- 추가 설정을 `redis.conf`에서 지정하면 `appendonly.aof`파일에 기록



#### 설치

> redis 설치

```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
```

- 이후 `make`, `make test`, `make install` 로 설치



> redis 서버 오픈

```
redis-server
```



> igbinary 설치

```bash
pecl install igbinary
```

- php에서 표준 직렬화를 사용하기 위한 패키지
- php extension에 `igbinary.so` 를 추가



> PHP redis 설치

```
pecl install redis
```

- `igbinary`와 `lzf` 압축 여부를 yes로 설정
- php extension에 `redis.so` 를 추가



> Predis 설치

- PHP용 Redis 클라이언트
- composer를 통해 설치

```
composer require predis/predis
```



> redis 시작, 종료

```bash
redis-server # redis 시작
redis-cli # redis 커맨드 라인 동작
redis-server <redis.conf 파일 위치> # 해당 설정으로 redis-server 시작
shutdown # redis종료
```



#### 특징

- 사용하기 전 추가로 redis 설치 필요
- in-memory 데이터 저장소기 때문에 접근 속도가 매우 빠르다
  - memcached와 유사한 속도
- AOF와 DB에 자료를 저장하기 때문에, 서버를 닫은 후 열어도 기존 데이터를 복구해서 사용할 수 있다.



#### memcached vs redis

|                  | memcached                   | redis                       |
| ---------------- | --------------------------- | --------------------------- |
| 저장공간         | memory                      | memory                      |
| 자료구조 지원    | 기본 자료형, 배열           | 대부분의 자료구조 지원      |
| 서버 재시작      | 데이터 유실                 | 데이터 보존                 |
| 메모리 효율성    | 효율적                      | 비효율적                    |
| 성능             | 멀티코어                    | 싱글코어                    |
| 데이터 저장 성능 | 대량의 데이터일 경우 효율적 | 소량의 데이터일 경우 효율적 |

- 둘 다 `key` - `value` 저장방식을 지원하지만, redis에 비해 memcached가 더욱 간단한 자료형 지원
- 따라서 memcached가 redis에 비해 메모리를 효율적으로 사용
  - 다만, redis가 hash 구조를 사용할 경우 memcached보다 효율적일 수 있다.



### 8. 속도 비교

- 35개의 레코드를 가져오는 상황

```php
public function getCache(Request $request) {
    $persons = Cache::remember('person', 1000, function() {
        return Person::all()->where('id', "<=", 35);
    });

    return response()->json($persons);
}
```



|          | no cache | file | array | database | memcached | redis |
| -------- | -------- | ---- | ----- | -------- | --------- | ----- |
| 시간(ms) | 941      | 643  | 940   | 686      | 641       | 655   |



### 9. Atomics-locks

- 경쟁 조건에 대한 걱정없이 분산 잠금장치 조작
- 분산 처리환경에서 캐시 저장소에 저장된 자원에 동시에 접근하려 할 때, 자원에 대한 사용을 관리
- Laravel에서 사용하기 위해 memcached나 Redis를 기본 드라이버로 사용해야 한다.



### 10. Cache Tag

- 캐시에 있는 관련 아이템들을 태그할 수 있다.
- 지정된 태그로 아이템을 저장, 수정, 조회, 삭제 할 수 있다.
- 태그를 통해 여러 태그에 한꺼번에 아이템 관련 연산이 가능
- 여러개의 태그를 한꺼번에 지정해도, 하나의 태그로는 접근이 불가능

```php
Cache::tags(['person', 'artists'])->put('john', "john", 3);  
$john = Cache::tags(['artists'])->get('john');

echo $john; # none
```



















