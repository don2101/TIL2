## Template Method Pattern

- 알고리즘의 일부 단계를 서브클래스화 하여 알고리즘의 부분적 정의 및 수정을 쉽게만든다
- 서브클래스를 재정의 하여 완전히 다른 기능이나 알고리즘 구현 가능
- 템플릿 메서드 패턴 알고리즘의 각 단계는 **개별적인 추상클래스**
  - 각 단계를 **원시 연산**이라고 한다.
  - 각 단계 마다 **추상 메서드**가 정의되어 있으며, 이를 모아 전체 알고리즘 구현



### 1. 기본 개념

#### 사용 상황

- 여러 **알고리즘** 또는 **클래스**가 **비슷하거나 같은 로직을 구현**할 때
- 알고리즘을 단계별로 **서브클래스화**해 코드의 중복을 줄일 수 있는 경우
  - 어떤 과정들에서 비슷한 로직이 존재할 때 이를 서브클래스화
    - ex) 차 끓이기 vs 커피 끓이기
- **서브클래스를 오버라이드**해 여러 알고리즘을 구현할 수 있는 경우



#### 사용 목적

- 알고리즘의 **뼈대**를 원시 연산으로 구현
- 구조를 수정하지 않고 일부 **서브클래스를 재정의**
- 코드의 재사용, 중복 최소화, **공통 인터페이스** 구현 및 사용
- 결국, **로직을 각 단계별로 쪼개 구현**하여 재사용 및 재구현 용이



### 2. 구조

#### 다이어그램

<img width="400" alt="template_method" src="https://user-images.githubusercontent.com/19590371/73364513-0f072e80-42ee-11ea-99fd-ed914c393b03.png">

- `AbstractClass`: 알고리즘의 단계를 정의하는 인터페이스
  - 각 단계를 정의하는 추상 메서드로 구성
  - 서브 클래스가 오버라이드

- `ConcreteClass`: 단계별 서브 클래스
  - 여러 추상 메서드로 구성된 알고리즘의 서브 클래스

- `template_method()`: 단계별 메소드를 호출하는 알고리즘 정의
  - 알고리즘의 뼈대를 정의



### 3. 구현 예시

#### 컴파일러

- 컴파일러는 **소스 파일**을 모아 바이너리 형태의 **오브젝트로 컴파일**
  - 이를 `collect_source()`, `coplite_to_object()` 두 추상 메서드로 정의
  - 실행하는 `run()` 메서드 구현
  - `complie_and_run()` 은 내부적으로 세 메서드를 호출

```python
from abc import ABCMeta, abstractmethod


class Compiler(metaclass=ABCMeta):
    @abstractmethod
    def collect_source(self):
        pass

    @abstractmethod
    def compile_to_object(self):
        pass

    @abstractmethod
    def run(self):
        pass

    def compile_and_run(self):
        self.collect_source()
        self.compile_to_object()
        self.run()


class iOSCompiler(Compiler):
    def collect_source(self):
        print("Collect Swift source")

    def compile_to_object(self):
        print("Compile code to bitcode")

    def run(self):
        print("Run program")


compiler = iOSCompiler()
compiler.compile_and_run()
```



> ##### 실행 결과

<img width="250" alt="스크린샷 2020-01-29 오후 11 14 45" src="https://user-images.githubusercontent.com/19590371/73364071-3dd0d500-42ed-11ea-896d-4c53769677b3.png">



#### 패키지 여행사

- 여행사는 고객이 선택할 패키지를 구성
- 패키지에는 방문할 장소, 교통 수단 등 여러 일정(단계)가 존재
- 고객은 취향에 따라 각 일정(단계)를 선택

```python
from abc import ABCMeta, abstractmethod


# Abstract Class 역할을 Travel 인터페이스
# 구현할 추상 메서드를 정의하여 제공
class Travel(metaclass=ABCMeta):
    @abstractmethod
    def set_transport(self):
        pass

    @abstractmethod
    def day1(self):
        pass

    @abstractmethod
    def day2(self):
        pass

    @abstractmethod
    def day3(self):
        pass

    @abstractmethod
    def return_home(self):
        pass

    def go_travel(self):
        self.set_transport()
        self.day1()
        self.day2()
        self.day3()
        self.return_home()


# Concrete Class 역할을 하는 KoreaTravel, JapanTravel
# Abstract Class를 구현하여, 여행일자(알고리즘의 각 단계)를 구현
class KoreaTravel(Travel):
    def set_transport(self):
        print("Take a bus for travel")

    def day1(self):
        print("Visit Seoul tower")

    def day2(self):
        print("Watch online game match")

    def day3(self):
        print("Buy some souvenirs at myungdong")

    def return_home(self):
        print("Return back to home with bus")


class JapanTravel(Travel):
    def set_transport(self):
        print("Take a subway for travel")

    def day1(self):
        print("Visit Tokyo tower")

    def day2(self):
        print("Enjoy Universal studio")

    def day3(self):
        print("Take a rest at japanese spa")

    def return_home(self):
        print("Return back to home with airplane")


# 알고리즘을 사용하는 Client 역할
class TravelAgency:
    def arrange_travel(self):
        self.korea_travel = KoreaTravel()
        self.japan_travel = JapanTravel()

        self.korea_travel.go_travel()
        self.japan_travel.go_travel()


TravelAgency().arrange_travel()
```



> ##### 실행 결과

<img width="261" alt="스크린샷 2020-01-29 오후 11 43 32" src="https://user-images.githubusercontent.com/19590371/73366369-314e7b80-42f1-11ea-94e7-f6571d9ea362.png">



### 4. 기타 내용

#### 후크(Hook)

- 서브클래스가 **알고리즘의 중간 단계를 제어**할 수 있는 기능 제공
  - ex) 여행에서 중간에 여행을 중단하거나 다른 루트로 가는 제어를 삽입 가능



#### 할리우드 원칙

- "먼저 연락하지 말고 기다리면 우리가 먼저 연락하겠습니다."
- 배우가 필요할 때 연락하는 방식
- 객체지향에서 하위 요소가 필요할 때 메인 시스템 중간에 들어갈 수 있다(Hook).
  - 다만 상위 요소가 언제 하위 요소가 필요한지 결정



#### 장단점

- 코드 중복이 줄어든다
- 상속으로 인한 코드 재활용 가능
- 서브 클래스 구현시 유연성 제공
- 코드 디버깅이 어려울 수 있다.
- 각 단계별로 영향을 준다면, 수정시 전체 알고리즘에 영향




