## Command Pattern

- 객체가 특정 기능을 바로 수행할 때 필요한 정보나 트리거에서 필요한 **정보**를 **캡슐화하는 행동 패턴**
- 캡슐화 하는 정보
  - 메소드**명**
  - 메소드를 **소유하는 객체**
  - 메소드 **인자**



#### 인스톨 위저드 예시

- 여러 단계를 거쳐 사용자에게 필요한 환경 설정을 파악
- 사용자는 단계별로 설정을 선택
- `Command` 객체를 실행하여 위저드 실행 후 사용자가 선택한 설정을 객체에 저장
- 인스톨을 수행하는 `execute()` 함수 호출
- 추가적으로, **프린터 스풀러**에서도 사용자가 선택한 설정을 `Command` 객체에 저장하고, 인쇄를 실행한다.



### 1. 구성 요소

- `Command`: `Receiver` 객체를 알고 있으며 `Receiver` 객체의 함수를 호출
- `Receiver`: 실행하는데 필요한 인자가 `Command` 에 저장되어 있다.
- `Invoker`: 명령을 수행
- `Client`: `Command` 객체를 생성하고 `Receiver` 를 정한다.



#### 목적

- `Client` 의 요청을 객체 속에 **캡슐화** 및 **매개변수화**
- 요청을 큐에 저장
- 콜백 지원



#### 사용하는 상황

- 수행하는 명령에 따라 **객체를 변수화** 할 때
- 요청을 큐에 저장하고 **다른 시점에 실행**해야 할 때
- 작은 단위 기반으로 **큰 상위 연산을 구성**할 때



### 2. 구조

![Command](https://user-images.githubusercontent.com/19590371/72812222-798fed00-3ca4-11ea-81b1-98a6b6afda92.png)

- `Command`: 연산을 수행할 인터페이스 정의 및 제공
- `ConcreteCommand`: `Receiver` 객체와 연산을 진행하는 바인딩 정의
- `Invoker`: `ConcreteCommand` 에 수행을 요청
- `Receiver`: 요청에 관련된 연산 수행
- `Client`: `ConcreteCommand` 객체 생성 및 `Receiver` 설정 

- `Client` 의 연산 요청 => `Invoker` 가 요청을 캡슐화하여 큐에 저장 => `Command` 는 요청의 수행을 `Receiver` 에게 맡긴다.





