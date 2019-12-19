## Unit Test

- 코드의 단위 기능마다 테스트를 진행하는 방식



### 1. 명심할 것

#### 단위는 프로그래밍 언어 마다 다르다.

- Java는 Class나 method가 단위가 될 수 있으며, Python은 function이 될 수도 있다.



#### 각 테스트는 독립적이어야 한다.

- **독립적**: 모든 테스트가 서로에게 **의존하지 않으며 격리**(isolation)되어야 한다.
  - 하나의 테스트는 하나의 기능만 검증
- **격리**: 테스트 대상(function, class...)을 실체하는 것이 아닌 **다른 어떤것으로 대체**하는 것
  - 이러한 대체제로 **Stub**, **Mock**, **Fake** 등이 있다.



#### 하나의 테스트는 단위 기능 중 **하나의 시나리오만 검증**

- 시나리오를 가정해보자...
  - 첫 파라미터가 Null
  - 두번째 파라미터가 Null
  - 두개 다 Null
  - 둘 다 정상인 경우 정상 작동
- 등의 시나리오중 하나의 시나리오만 검증하도록 한다.



### 2. Test Double

- 테스트 대상을 격리(가상의 객체로 대체)하는 대체제
- Stub, Mock, Fake등을 지칭한다.



> #### 왜 사용하는가?

- 실제로 하나의 메서드가 다른 네트워크, DB 등등에 의존하고 있다면 테스트 하기가 어렵다.
- 즉, 하나의 기능이 다른 시스템에 얽혀있고 의존하고 있다면 테스트하기가 매우 어렵다.
- 실제 객체를 사용하여 테스트 하기에 Cost가 많이 발생하기 때문에 **가짜 객체**를 만들어 테스트를 대체



> #### 실제 객체를 테스트 더블로 대체하면...

1. 실제 행위를 수행하는 것이 아닌 검증만 하기 때문에 테스트 속도 개선
2. 예측 불가능한 실행 요소 제거
3. 특수한 상황을 시뮬레이션 가능



#### Mock

- 행위 검증에 사용하는 테스트 더블



#### Stub

- 상태 검증에 사용하는 테스트 더블
- 미리 준비된 답변(canned answer)을 return하여 테스트를 진행



### 3. Mock을 사용한 테스트

##### 사람이 전화기를 사용하여 메세지를 전하는 경우

```java
public class Person {
    private Cellphone cellphone;
    
    public Person(Cellphone cellphone) {
        this.cellphone = cellphone;
    }
    
    public call(String message) {
        this.cellphone.send(message);
    }
}
```

- `Person`의 `call()` 메서드에 대한 검증을 하려면 어떤 것을 검증해야 할까?
- 실제로 `message`를 보냈는지는` call()` 메서드에서 검증해야 할 부분이 아니다.
  - `message`를 제대로 보냈는지는 `send()` 메서드에서 검증해야 될 문제
- `call()`메서드에서 확인해야 하는 것은 **message를 send()메서드에 제대로 전달했는지** 이다.
- `call()`메서드의 책임은 그것뿐이며, 하나의 시나리오만 검증한다.



##### Mock을 생성하여 Test

```java
public class CellphoneMock extends Cellphone {
    private boolean isMessageCalled = false;
    private String message = "";
    
    @override
    public send(String message) {
        this.isMessageCalled = true;
        this.message = message;
    }
    
    public boolean isMesageCalled() { return this.isMessageCalled; }
    public String getMessage() { return this.message; }
}
```

- 실제 테스트에서 `Cellphone`과 같은 유형의 객체여야 하기 때문에 `Cellphone`객체를 상속받아 `send()` 메서드를 재정의
- 행위 검증만 하기 때문에 실제 코드를 실행 시킬 필요가 없고, 부모에서 정의한 `send()`는 호출하지 않는다.
- 행위 검증을 위해 메세지와 메세지 호출 여부만 저장
- 실제 로직을 실행하지는 않기 때문에 더 빠르게 테스트 가능



### 4. Stub을 사용한 테스트

#### stub를 사용하는 상황

- 호출하려는 함수가 아직 구현되지 않았을 때
  - ex) 프론트 엔드에서 서버에 요청을 하고 싶은데 해당 메서드가 구현되지 않은 경우
- 함수 호출 비용이 큰 경우
  - 함수가 하드웨어나 네트워크 접근 등에 종속되어 있는 경우  테스트 환경 구축이 어렵다
- 위험 부담이 큰 테스트인 경우
  - 레지스트리나 DB 설정등의 변경이 필요한 경우 등 예민한 설정이 필요한 경우 stub을 사용하여 우회
- 실행 흐름에 대해 해당 기능만 독립적으로 테스트할 때



##### 서버에서 데이터 전송을 위한 인터페이스 정의

```java
public Result sendData(String data);
```



##### 프론트엔드에서 해당 인터페이스를 통해 데이터 업로드 구현

```javascript
function upload (data) {
    result = sendData(data);
    
    if (result.resultCode == 0) {
        //...
    } else {
        //...
    }
}
```



> 문제점...

- 해당 인터페이스가 구현되지 않았다면 테스트 불가
- 구현 되었어도 서버측 네트워크 구성이 안되어 있거나, 서버가 열려있지 않다면 테스트 불가
- 서버와의 연동 시간에 따라 테스트 시간이 길어진다.
- `sendData`에 위험 요소가 있다면 테스트가 어렵다.



##### sendData에 대한 stub를 작성하여 테스트 우회

```javascript
// 성공하는 경우
function uploadData(data) {
    result.resultCode = 0;
    result.resultMessage = "Success";
    
    return result;
}

// 실패하는 경우
function uploadData(data) {
    result.resultCode = 1;
    result.resultMessage = "Fail";
    
    return result;
}
```

- `sendData`에 대한 stub를 만들어 `result`를 받는 상황을 **가정**
- `result`로 올 수 있는 결과를 미리 만들어 테스트를 진행





> ### Refs.

[Stub는 언제 사용]( https://m.blog.naver.com/PostView.nhn?blogId=suresofttech&logNo=221204092938&proxyReferer=https%3A%2F%2Fwww.google.com%2F )

[Mock의 개념]( https://www.crocus.co.kr/1555 )

[Test Stub]( [https://medium.com/@SlackBeck/%ED%85%8C%EC%8A%A4%ED%8A%B8-%EC%8A%A4%ED%85%81-test-stub-%EC%9D%B4%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80-ff9c8840c1b0](https://medium.com/@SlackBeck/테스트-스텁-test-stub-이란-무엇인가-ff9c8840c1b0) )

[Mock이란?]( [https://medium.com/@SlackBeck/mock-object%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80-85159754b2ac](https://medium.com/@SlackBeck/mock-object란-무엇인가-85159754b2ac) )

