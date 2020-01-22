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

- `Client` 의 요청을 객체 속에 **캡슐화** 및 **매개변수화** 하여 다양한 상황에 사용
- 요청을 큐에 저장
- 객체지향 콜백 지원



#### 사용하는 상황

- 수행하는 명령에 따라 **객체를 변수화** 할 때
- 요청을 큐에 저장하고 **다른 시점에 실행**해야 할 때
- 작은 단위 기반으로 **큰 상위 연산을 구성**할 때



### 2. 구조

![Command](https://user-images.githubusercontent.com/19590371/72900161-ba523980-3d6a-11ea-9a5c-344184e0fa5d.png)

- `Command`: 기능을 수행할 인터페이스 정의 및 제공
- `ConcreteCommand 1, 2, ...`: `Receiver` 객체를 저장하고 인터페이스를 통해 수행할 기능을 캡슐화하여 저장
- `Invoker`: 클라이언트가 직접 호출하여, `ConcreteCommand` 에 기능 수행을 요청
- `Receiver 1, 2, ...`: 요청에 관련된 실제 기능을 수행
- `Client`: `ConcreteCommand` 객체 생성 및 `Receiver` 설정. `Invoker` 호출 

- `Client` 의 기능 수행 요청 => `Invoker` 가 요청을 캡슐화하여 큐에 저장 => `Command` 는 요청의 수행을 `Receiver` 에게 맡긴다.



#### 예시 구현

```python
from abc import ABCMeta, abstractmethod


# 구현될 Command. 실제 수행될 행동에 대한 인터페이스 제공
class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


# 구현된 Command. 각 기능에 따라 Recevier를 받아 저장하고, 해당 기능을 수행을 캡슐화
class ConcreteCommand1(Command):
    def __init__(self, flasher):
        self.flasher = flasher

    def execute(self):
        self.flasher.light_on()


class ConcreteCommand2(Command):
    def __init__(self, watergun):
        self.watergun = watergun
        
    def execute(self):
        self.watergun.shoot_water()       


# Receiver 역할을 하는 Flasher와 Watergun. 실제 기능을 수행
class Flasher:
    def light_on(self):
        print("Light on")


class Watergun:
    def shoot_water(self):
        print("Shoot water")


class Invoker:
    def set_command(self, command):
        self.command = command

    def execute(self):
        self.command.execute()


if __name__ == '__main__':
    flasher = Flasher()
    watergun = Watergun()

    command1 = ConcreteCommand1(flasher)
    command2 = ConcreteCommand2(watergun)

    invoker = Invoker()
    invoker.set_command(command1)
    invoker.execute()
    invoker.set_command(command2)
    invoker.execute()
    invoker.set_command(command1)
    invoker.execute()
```

- 여러개의 `Receiver`(`Watergun`, `Flahser`) 를 정의
- `Command` 를 상속받은 `ConcreteCommand 1, 2` 를 구현하고, `Receiver` 를 캡슐화
- `Invoker` 는 상황에 따라 다른 `Command` 와 연결하여 각 `ConcreteCommand` 를 통해 `Receiver` 실행



> ##### 실행 결과

<img width="150" alt="스크린샷 2020-01-22 오후 11 18 47" src="https://user-images.githubusercontent.com/19590371/72901707-8fb5b000-3d6d-11ea-8aaf-80d7b0b8b285.png">



> #### 예시에서 Command가 없었다면...

- 하나의 `Invoker` 로 두 가지 기능을 처리할 수 없다
  - 따라서, 각 `Receiver` 마다 이를 실행할 `Invoker` 가 매 번 필요하게 되고 잦은 코드 수정으로 이어진다.



### 3. 증권거래소 예시

- 브로커가 클라이언트와 거래소 사이에서 중개자 역할을 수행
- 중개자는 클라이언트가 주식 거래 요청시 이를 큐에 저장한 후 실행

```python
from abc import ABCMeta, abstractmethod


# Command 역할을 하는 Order. 메서드 인터페이스를 제공
class Order(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


# ConcreteCommand 역할을 하는 Buy/SellStockOrder
# 수행할 기능을 캡슐화 하여 저장
# Receiver를 저장하고 기능 수행을 Receiver에게 맡긴다
class BuyStockOrder(Order):
    def __init__(self, stock):
        self.stock = stock

    def execute(self):
        self.stock.buy()


class SellStockOrder(Order):
    def __init__(self, stock):
        self.stock = stock
    
    def execute(self):
        self.stock.sell()


# Receiver 역할을 하는 StockTrade. 실제 기능을 수행
class StockTrade:
    def buy(self):
        print("Buy stocks")

    def sell(self):
        print("Sell stocks")


# Invoker 역할을 수행하는 Agent
# 유저의 요청을 큐에 저장한 뒤 실행하고 제거
class Agent:
    def __init__(self):
        self.__order_queue = []

    def add_order(self, order):
        self.__order_queue.append(order)
        order.execute()
        self.__order_queue.pop()


if __name__ == '__main__':
    stock = StockTrade()
    buy_stock = BuyStockOrder(stock)
    sell_stock = SellStockOrder(stock)

    agent = Agent()
    agent.add_order(buy_stock)
    agent.add_order(sell_stock)
    agent.add_order(buy_stock)
    agent.add_order(sell_stock)

```



> ##### 실행 결과

<img width="140" alt="스크린샷 2020-01-23 오전 12 00 43" src="https://user-images.githubusercontent.com/19590371/72905160-6bf56880-3d73-11ea-960b-fc328a2857a7.png">



### 4. 기타 내용

#### 실제 적용 상황

- 커맨드 패턴을 사용하여 `Redo` 나 `Rollback` 명령어를 저장하고, 필요할 때 마다 명령을 순차적으로 실행
- 분산환경에서 코어서비스에 요청이 몰리지 않도록 비동기로 작업 수행
  - `Invoker` 객체를 통해 모든 요청을 큐에 저장하고 순차적으로 `Recevier` 객체에 보내 메인 스레드로 부터 독립적으로 수행



#### 장단점

- 작업 요청 클래스와 수행 클래스를 분리
- 큐에 명령을 저장하여 수행
- 기존 코드를 수정하지 않고 커맨드 추가 가능
- 객체가 많아지면 관리가 힘들 수 있다.
- 모든 작업이 독립적이므로 유지 보수에 많은 비용 소모

