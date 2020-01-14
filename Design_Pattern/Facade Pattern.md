## Facade Pattern

### 1. Structural Design Pattern

- 구조 디자인 패턴은 객체 클래스와 병합하여 더 큰 구조를 만든다
- 구조 패턴: 클래스 패턴과 객체 패턴을 합친 개념
  - 클래스 패턴: 상속을 통해 객체를 추상화 하여 인터페이스 제공
  - 객체 패턴: 한 개의 객체를 더 큰 객체로 확장



#### 구조 디자인 패턴 종류

- Adapter Pattern: 사용자의 요구에 따라 특정 인터페이스를 다른 인터페이스에 맞춘다.
  - 서로 다른 클래스 인터페이스를 **목적에 맞춰 변환**
- Bridge Pattern: 객체의 인터페이스와 구현을 분리해 독립적으로 동작하게 한다.
- Decorator Pattern: 런타임에 객체의 책임(속성 등)을 추가한다.
  - 인터페이스를 통해 **객체에 속성을 추가**



### 2. Facade

- 건물의 정면, 보이는 쪽. 외관
- 복잡한 내부 구조, **시스템 로직을 감추고** 사용자가 **시스템에 쉽게 접근할 수 있는 인터페이스 제공**



#### 목적

- 서브 시스템의 **인터페이스를 통합**시킨 단일 인터페이스를 제공
  - 사용자가 쉽게 서브 시스템에 접근
- 단일 인터페이스 객체로 복잡한 서브 시스템 대체
  - 서브 시스템 **캡슐화가 아닌 결합**
- 사용자와 내부 구현을 분리



### 3. 구조

#### Client

- 복잡한 내부 시스템 구조를 알 필요 없이 서브 시스템과 통신하는 개체
- 퍼사드를 인스턴스화 하는 클래스
- 퍼사드에게 작업 수행을 요청



#### Facade

- 복잡한 서브 시스템을 외부에서 보기에 깔끔하게 감싸는 역할
- 요청에 적합한 서브 시스템을 알고 있는 인터페이스
  - 컴포지션을 통해 클라이언트의 **요청을 적합한 서브 시스템에 전달**



#### System

- 전체 시스템을 하나의 복합체로 만드는 여러 **서브 시스템의 집합**
- 서브 시스템의 기능을 구현하는 클래스
- 퍼사드를 참조하지 않으며, 존재를 알지 못한다.



> ##### => 복잡한 일을 일일이 찾아서 하지 말고, 하나로 묶어 상황에 따라 업무를 처리



##### 결혼식 준비 예시

> ##### Facade 역할을 하는 EventManager

```python
class EventManager(object):
    def __init__(self):
        print("Let me talke to the folks")

    def arrangeWedding(self):
        self.hotelier = Hotelier()
        self.hotelier.bookHotel()

        self.florist = Florist()
        self.florist.setFlower()

        self.caterer = Caterer()
        self.caterer.setFoods()

        self.musician = Musician()
        self.musicain.playMusic()

```

- `EventManager` 는 `Facade` 역할을 맡아 여러 복잡한 결혼 준비 작업을 처리한다.
- `Client` 를 위해 간소화된 인터페이스를 제공
- 컴포지션을 통해 `SubSystem` 객체를 생성



> ##### (Sub)System역할을 하는 클래스들

```python
class Hotelier(object):
    def __init__(self):
        print("Booking hotel...")

    def book_hotel(self):
        print("Registered the booking")
    

class Florist(object):
    def __init__(self):
        print("Preparing flowers...")

    def set_flower(self):
        print("Prepared flowers")


class Caterer(object):
    def __init__(self):
        print("Preparing foods...")

    def set_foods(self):
        print("Prepared foods")


class Musician(object):
    def __init__(self):
        print("Preparing for music...")

    def play_music(self):
        print("Played music")
```

- 모든 결혼 준비에 대한 작업을 명시(`SubSystem`)



> ##### 작업을 지시하는 Client

```python
class Client(object):
    def __init__(self):
        print("Decide EventManager")
        self.event_manager = EventManager()

    def ask_wedding_arrange(self):
        self.event_manager.arrange()


client = Client()
client.ask_wedding_arrange()
```

- 복잡한 결혼 준비 절차를 모른채, 모든 작업을 `EventManager(Facade)` 에게 지시



> ##### 실행 결과

<img width="205" alt="스크린샷 2020-01-14 오후 10 36 10" src="https://user-images.githubusercontent.com/19590371/72348810-8fd6ff80-371e-11ea-91d4-56bcf5a9f832.png">



### 4. 정리

#### Principle of least knowledge

- 파사드 패턴은 위 원칙에 기반하여 설계
- 상호 작용 하는 객체를 **가까운 몇 개의 객체**로 제한
- 시스템을 설계할 때 모든 객체가 연관된 클래스와 어떤 식으로 대화하는지 안다
- 원칙에 따라 지나치게 얽혀있는 클래스를 만드는 것을 지양한다.
- 클래스간 의존도를 낮춘다.



#### 파사드 패턴 단점

- 어플리케이션에 필요 없는 여러 개의 인터페이스가 존재하면 
  - 시스템 복잡도가 상승하고, 
  - 런타임 성능이 저하된다.



#### 파사드 패턴...

- 클라이언트에게 간소화된 통합된 서비스에 대한 인터페이스 제공
- 시스템의 복잡성을 줄여 클라이언트의 일을 줄인다.

