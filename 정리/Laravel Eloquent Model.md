## Eloquent ORM

- DB와 작동하여 테이블을 조작하는 ORM
- DB 테이블과 연동되는 모델이 있다.



### 1. Eloquent 모델 정의

- ORM과 연동되는 Model 정의
- 기본적으로 `app`디렉토리에 존재해야 하지만 `composer.json`에서 오토로드 되는 곳이라면 상관없다.



#### Artisan command 사용

```bash
php artisan make:model 모델명 -m 
```

- `-m`을 붙이면 마이그레이션을 같이 생성



#### Table 이름 명시

- 모델이 어떤 DB 테이블을 사용할 지 알려주어야 한다

```php
class Post extends Model
{
    protected $table = 'posts';
}

```

- 그렇지 않으면 클래스의 스네이크 케이스로 복수형의 이름이 사용된다.



#### Primary key

- 기본적으로 auto increment하는 정수형 id를 부여

```php
protected $incrementing = false; # auto increment 취소
protected $keyType = 'string' # key type 변경
```



#### Timestamp

- 모델 생성시 자동으로 `updated_at`, `created_at` 컬럼을 추가
- 사용하지 않거나 `$dateFormat` 필드를 수정하여 날짜 형식을 변경할 수 있다.



#### Database Connection

- 기본 커넥션을 사용하여 `$connection` 필드를 통해 다른 커넥션 사용 가능



#### Default value

- 기본 속성값 정의

```php
protected $attributes = [
    'title' => 'default title',
]
```



### 2. 모델 연산

#### 조회

```php
use App\Post;

Post::all();
```

- `Post` 모델의 모든 레코드 조회



#### 제약조건 추가

- Eloquent 모델이 **쿼리 빌더**역할을 하기 때문에 조건을 추가하여 조회 가능

```php
$posts = Post::where('id', '>=', $postNum)->take(10)->get();
```



#### Model Fresh, Refresh

- `fresh`: 해당 인스턴스를 검색할 때 사용했던 동일한 쿼리를 날려 동일한 결과를 검색 
  - 기존 인스턴스에 영향 X

```php
$post = Post::where('id', '=', $postNum)->first();
# title 21content 21
$newPost = $post->fresh();
# title 21content 21
```

- `refresh`: DB의 새로운 데이터를 검색하여 기존 모델 갱신

```php
$post = Post::where('id', '=', $postNum)->first();
$post->title = "new title";
echo '<p>' . $post->title . $post->content . '</p>';
# new titlecontent 21

$post = $post->refresh();
echo '<p>' . $post->title . $post->content . '</p>';
# title 21content 21
```



#### Collection

- `all` 이나, `get` 같이 여러 레코드를 가져오는 메서드는 `Illuminate\Database\Eloquent\Collection` 인스턴스를 반환



#### Chunk

- 수많은 레코드를 조회할 때 결과를 분할하여 가져오는 메서드
- 정해진 갯수만큼 분할된 Eloquent 모델들을 가져오며, `closure` 에 의해 처리
- 많은 쿼리를 가져올 때 메모리를 절약하기 위해 사용

```php
public function getChunk(Request $request, $chunkNum) {
    Post::chunk($chunkNum, function ($results) {
        foreach ($results as $result) {
            echo '<p>' . $result->title . $result->content . '</p>';
        }
    });
}
```

- 정해진 `$chunkNum` 만큼의 결과를 반복해서 가져온다.
- callback 형식으로 레코드에 대한 연산 지정



#### Cursor

- 하나의 쿼리를 실행하는 커서를 통해 DB 레코드 전체를 iterating 가능
- 대량의 데이터를 처리하는 경우에 메모리 사용량을 줄인다.

```php
public function getCursor(Request $request) {
    Log::info("Get Cursor!");
    foreach(Post::where('id', '>=', 1)->cursor() as $result) {
        echo '<p>' . $result->title . $result->content . '</p>';
    }
}
```

- `all()` 메서드를 통해 `cursor()`를 사용할 수 없다.





