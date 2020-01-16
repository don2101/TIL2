## Proxy Pattern

### 1. Proxy

- 요청자와 공급자 사이의 **중재자, 대리자**



#### 웹 관점 프록시 서버

  1. 클라이언트가 리소스 요청
  2. 프록시 서버에서 요청을 분석하여 적절한 서버에서 요청 송신
  3. 서버에서 제공하는 리소스를 클라이언트에게 전달

- **요청을 캡슐화**하여 안전하며, **분산 시스템 구조**에 적합



#### 디자인 패턴 관점 프록시 클래스

- 객체의 인터페이스 역할
  - 객체: 네트워크 연결 또는 메모리, 파일에 저장된 객체 등
- 반환하여 사용할 **객체를 감싸는** 역할
- 객체 구현과 상관 없이 객체에 대한 기능 제공
- 주 목적: 실제 객체에 접근할 수 있는 **대리 객체나 껍데기** 제공



#### 프록시의 역할

- 복잡한 시스템을 **간단하게 표현**
- 특정 객체의 **대리 객체**를 제공하여 접근 제어
- 객체에 대한 **보안** 제공
  - 클라이언트가 객체에 직접 접근하는 것을 막아 보안 강화
  - 의도하지 않는 케이스로 부터 객체 보호
- 분산 구조를 지원하기 위한 **레이어, 인터페이스** 제공
  - 다른 서버에 있는 **외부 객체에 대한 로컬 인터페이스** 제공
  - 분산 시스템 구조에서 클라이언트가 원격으로 작업시 로컬 객체(프록시)에게 요청을 보내 대리 수행
- 메모리 사용량이 높은 객체를 다루는 **핸들러** 역할
  - ex) 사진에 대한 썸네일을 먼저 제공



### 2. 구조

![Proxy](https://user-images.githubusercontent.com/19590371/72440032-6df77e80-37eb-11ea-99d8-d68aed06be91.png)



- `Proxy`: `Real Object` 에 접근할 수 있는 인터페이스 제공, 실 객체를 대체
  - `Object`와 동일한 인터페이스를 가지므로 `Object` 를 대체할 수 있다.
- `Object`: `Real Object` 와 `Proxy` 가 구현하는 인터페이스
  - `Object` 와 `Proxy` 가 같은 인터페이스를 구현하기 때문에 `Proxy` 가 대체할 수 있다.
- `Real Object`: `Client` 가 요청하는 실제 객체



### 3. 상황 예시

#### 배우와 에이전트 예시

1. 영화사가 배우를 모집할 때 배우에게 직접 연락하는 것이 아닌 **에이전트를 통해 연락**

2. 에이전트는 배우의 상황에 따라 출연 여부를 **대신 통보**

- 에이전트가 배우와 영화사 사이에서 대리 객체, 전달자 역할

```python
# 객체 역할을 하는 배우
class Actor(object):
    def __init__(self):
        self.isBusy = False

    def acting(self):
        self.isBusy = True
        print(type(self).__name__, "is busy")


    def available(self):
        self.isBusy = False
        print(type(self).__name__, "is free")

    def get_status(self):
        return self.isBusy


# 배우에 대한 대리 자
# 배우에 대한 접근 제어 및 상태 전달
class Agent(object):
    def __init__(self):
        pass

    def work(self, actor):
        self.actor = Actor()

        if self.actor.get_status():
            self.actor.acting()

        else:
            self.actor.available()


if __name__ == '__main__':
    agent = Agent()
    agent.work()

```



#### 결제 시스템

- 현금 카드를 사용하면, 카드 정보를 입력하기만 해도 판매자의 계좌로 돈이 인출된다.

```python
from abc import ABCMeta, abstractmethod


# Object 역할
# Bank와 DebitCard가 구현하는 인터페이스
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def do_pay(self):
        pass


# Real Object 역할
class Bank(Payment):
    def __init__(self):
        self.card = None
        self.account = None

    def __get_account(self):
        self.account = self.card

        return self.account

    def __check_money(self):
        print("Check", self.__get_account(), "has enough money")

        return True

    def set_card(self, card):
        self.card = card

    def do_pay(self):
        if self.__check_money():
            print("Bank made payment")
            
            return True
        else:
            print("At bank Not enough money")        

            return False


# Bank를 대신해 결제를 대신하는 Proxy
class DebitCard(Payment):
    def __init__(self):
        self.bank = Bank()

    # Bank에 직접 접근하지 않고 Bank를 대신해 결제 진행
    def do_pay(self):
        card_number = 12345
        self.bank.set_card(card_number)

        return self.bank.do_pay()


class Client(object):
    def __init__(self):
        print("Wanna buy a shirt")
        self.debit_card = DebitCard()
        self.is_purchasable = None

    def make_payment(self):
        self.is_purchasable = self.debit_card.do_pay()

    def __del__(self):
        if self.is_purchasable:
            print("Buy a shirt")
        else:
            print("Not enough money")


client = Client()
client.make_payment()
```

- `Object` 역할을 하는  `Payment` 를 `DebitCard` 와 `Bank` 가 구현
- `DebitCard` 는 결제 요청이 들어오면 `Bank` 를 대신해 결제 수행



> ##### 구매 가능한 경우

<img width="300" alt="스크린샷 2020-01-15 오후 11 38 42" src="https://user-images.githubusercontent.com/19590371/72442618-2cb59d80-37f0-11ea-9350-2c37c8d527ce.png">



> ##### 돈이 부족한 경우

<img width="300" alt="스크린샷 2020-01-16 오후 10 20 08" src="https://user-images.githubusercontent.com/19590371/72528479-6ea51900-38ae-11ea-8b86-1d806d0db081.png">





### 4. 여러 유형의 프록시

- 다양한 상황에서 다양한 종류의 프록시를 사용



#### Virtual Proxy

- 인스턴스화 하는데 비용이 많이 소모되는 **객체를 대체 혹은 제어**하는 역할
  - ex) 웹 서비스에서 용량이 큰 이미지를 작은 이미지로 대체하고, 사용자가 접근 시 실 객체 생성



#### Remote Proxy

- 원격 서버나 다른 주소 공간에 있는 객체애 대한 **로컬 인터페이스** 제공
  - ex) 다수의 웹, DB, 작업, 캐시 서버 등의 시스템을 모니터링 할 때 원격 명령 수행을 **원격 프록시 객체**를 통해 수행



#### Protective Proxy

- 실 객체의 중요 부분에 대한 접근 제어
  - ex) 웹 서비스에서 사용자 인증, 인가 담당 프록시 서버



#### Smart Proxy

- 사용자가 객체에 접근했을 때 추가적인 행동을 수행

  - ex) 동시에 중앙 객체에 요청이 들어왔을 때 

    직접 기능을 수행하기 보다 스마트 프록시가 객체의 잠금 상태를 확인해 접근 제어



### 5. 정리

#### 프록시 패턴의 장점

- 자주 사용되는 무거운 객체를 캐싱하여 어플리케이션 성능 향상
- 실 객체에 대한 접근 요청 인증
- 원격 서버 간의 네트워크 연결, DB 연결 구현에 프록시 패턴이 적합하며, 모니터링 용도로도 구현할 수 있다.



#### 단점

- 접근 제어, 인증 등으로 인해 응답시간이 길어질 수 있다.
  - 따라서 제대로 설계해야 한다.



#### Facade vs Proxy

- 둘 다 구조 패턴으로 비슷해 보이지만 **사용하는 목적**이 다르다.

| Facade                                                       | Proxy                                                 |
| ------------------------------------------------------------ | ----------------------------------------------------- |
| 실 객체에 대한 대리 객체를 제공해 **접근 제어**              | 클래스의 서브 시스템에 대한 **인터페이스 제공**       |
| 타겟 객체와 동일한 인터페이스 구조이며, 타겟 객체에 대한 참조를 갖는다. | 서브 시스템간의 의존도와 통신을 최소화 하기 위해 사용 |
| 클라이언트와 실 객체 사이의 중간자 역할                      | 하나의 통합된 객체 제공                               |





