## State Design Pattern

- 행위 패턴의 한 종류
- **런타임**에 객체의 행위를 변경
- 상황에 따라 객체의 행동 방식을 변경
- 한가지 메서드로 상황에 따라 다른 결과 도출
- 객체의 **상태에 따라 행위가 결정**된다.
- ex) 라디오
  - 라디오의 상태 (AM/FM)에 따라 주파수 스캔 방식(AM/FM)이 나뉜다.



###1. 구조 /. 구성 요소

![state_pattern](https://user-images.githubusercontent.com/19590371/73847365-792d4f80-4869-11ea-8b60-a8a63595b027.png)

- `State`: 객체의 **행위를 캡슐화** 하는 인터페이스
  - `ConcreteSTate` 가 구현할 메서드(`Handle()`) 정의
- `ConcreteState`: `State` 인터페이스를 구현하는 서브클래스. 특정 상태의 객체 행위를 구현
  - `State` 의 설정에 따라 실행된 각 `Handle()` 메서드를 구현
- `Context`: 사용자가 선택한 인터페이스를 정의
  - 사용자의 요청을 넘겨 받는 클래스
  - 객체의 현재 **상태를 저장**하고, 요청에 맞는 **메소드 호출**



### 2. 예시 코드

#### State Design Pattern 구현

```python
from abc import ABCMeta, abstractmethod


class State(metaclass=ABCMeta):
    @abstractmethod
    def Handle(self):
        pass


class ConcreteStateA(State):
    def Handle(self):
        print("Call State A")


class ConcreteStateB(State):
    def Handle(self):
        print("Call State B")


# state 를 저장하고 상황에 따라 다른 함수 호출
class Context(State):
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def Handle(self):
        self.state.Handle()


context = Context()
state_a = ConcreteStateA()
state_b = ConcreteStateB()

context.set_state(state_a)
context.Handle()
context.set_state(state_b)
context.Handle()

```



> ##### 실행 결과

<img width="200" alt="스크린샷 2020-02-05 오후 10 56 56" src="https://user-images.githubusercontent.com/19590371/73848114-d7a6fd80-486a-11ea-9846-c54db64f0c1a.png">



#### TV 상태에 따라 키고 끄기

```python
from abc import ABCMeta, abstractmethod


class TVState(metaclass=ABCMeta):
    @abstractmethod
    def press_button(self):
        pass


class TVoff(TVState):
    def press_button(self):
        print("Turn on TV")


class TVon(TVState):
    def press_button(self):
        print("Turn off TV")


class RemoteController(TVState):
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def press_button(self):
        self.state.press_button()


remote_controller = RemoteController()

on = TVon()
off = TVoff()

remote_controller.set_state(on)
remote_controller.press_button()
remote_controller.set_state(off)
remote_controller.press_button()

```

- TV 리모컨은 TV가 켜져있는지 여부에 따라 다른 행위(끄기, 크기)를 수행
- TV의 상태에 따라 하나의 행위(`press_button()`) 이 다른 동작을 수행한다.
  - 버튼은 하나를 누르지만 2가지 동작을 수행



> ##### 실행 결과

<img width="200" alt="스크린샷 2020-02-05 오후 11 05 30" src="https://user-images.githubusercontent.com/19590371/73848733-0671a380-486c-11ea-9c2a-b037d0cd365c.png">



#### Computer 상태 변환

```python
# 각 컴퓨터의 상태에 따라 허용된 상태 변화를 정의 하는 State 역할의 인터페이스
# 인터페이스에서 ConcreteState를 제어
class ComputerState(object):
    name = None
    allowed = []

    def switch(self, state):
        if state.name in self.allowed:
            print('switch', self, ' to new state ', state.name)
            self.__class__ = state
        else:
            print(self, ' to new state ', state.name, ' is not possible')

    def __str__(self):
        return self.name
    

# ConcreteState 역할을 하는 클래스
# name: 현재 상태, allowed: 현재 상태에서 변화할 수 있는 상태
class Off(ComputerState):
    name = "off"
    allowed = ["on"]

    
class On(ComputerState):
    name = "on"
    allowed = ["off", "suspend", "hibernate"]

    
class Suspend(ComputerState):
    name = "suspend"
    allowed = ["on"]

    
class Hibernate(ComputerState):
    name = "hibernate"
    allowed = ["on"]


# Context 역할을 하는 클래스
class Computer(object):
    def __init__(self):
        self.state = Off()

    def change(self, state):
        self.state.switch(state)


# 클래스 자체를 삽입하여 State를 동적으로 변화
computer = Computer()
computer.change(On)
computer.change(Off)
computer.change(On)
computer.change(Suspend)
computer.change(Hibernate)
computer.change(Off)
computer.change(On)
computer.change(Suspend)
computer.change(Hibernate)

```

- 컴퓨터는 4가지 상태(on, off, suspend, hibernate)가 있으며 각 상태마다 변형할 수 있는 상태가 다르다
- `State` 인터페이스에서 변화할 수 있는 상황을 제어하여 컴퓨터 상태를 변경



##### \__class__ 속성

- **클래스 자기 자체**를 참조할 때 사용하는 속성
- `self.__class__.name` 은 클래스 자체의 이름을 출력
- 예시에서 클래스(`State`)를 삽입하여 객체의 클래스(`ComputerState`)를 동적으로 런타임에 변경한다.



> ##### 실행 결과

<img width="360" alt="스크린샷 2020-02-05 오후 11 19 46" src="https://user-images.githubusercontent.com/19590371/73849868-02df1c00-486e-11ea-804c-90a8fb2ad13a.png">



### 3. 장단점

- 상태 패턴에서 객체의 행위가 해당 상태의 실행 함수의 결과 값과 같다.
  - 상태를 런타임에 변경되며, 분기문(`if/else`) 등의 사용을 줄일 수 있다.
- 다형성 구현을 쉽게 할 수 있다.
- 새로운 `ConcreteState` 를 추가하여 새로운 기능을 쉽게 추가할 수 있다.
- 쓸데없는 클래스 남발
- 행위를 추가한 뒤 `Context` 또한 변경해야 한다.

