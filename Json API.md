##Json API

### 1. Json

- 클라이언트와 서버간 데이터를  전달하는 포맷중 하나
- JavaScript Object Notation의 약자이며 다음과 같은 특징이 있다.



#### 특징

- 이름에서 알 수 있듯이 쉽게 Javascript Object로 변활할 수 있으며, Javascript를 사용하는 클라이언트간 데이터 전송이 용이하다.
- 
- Javascript 문법과 유사하지만, 텍스트 형식일 뿐이다. 
- 데이터 포맷일 뿐이며, 메서드를 포함할 수 없다.
- Key-Value 형태로 데이터를 



### 2. Json  API

- 클라이언트와 서버가 Json으로 데이터를 주고 받기 위해 지켜야할 몇 가지 명세가 있다.



#### 클라이언트

- 요청 헤더에 `Content-Type: application/vnd.api+json`를 명시하여 데이터를 전송한다.



#### 구조

- Json object는 응답 요청 데이터의 최상위에 위치한다.
- 다음의 세가지 데이터를 포함한다.
  - data: 전달하는 데이터 object
  - error: 에러가 발생했을 시 전달하는 object
  - meta: 메타 정보를 포함하는 object
- data와 error는 동시에 전달할 수 없다.
- 추가적으로 다음의 데이터는 포함 시킬 수 있다.
  - jsonapi: 서버의 스펙을 담는다. 



