## Factory Pattern

#### Factory

- 다른 클래스의 객체를 생성하는 클래스
- 특정 객체가 메서드를 호출하면 팩토리가 해당 객체를 생성 후 반환한다.



#### 장점

- 객체 생성과 클래스 구현 로직을 나눠 상호 의존도를 줄인다.
- 생성하려는 객체 클래스 구현과 상관없이 사용 가능
- 코드를 수정하지 않고, 팩토리에 새로운 클래스를 추가할 수 있다.
- 이미 생성된 객체를 팩토리가 재활용 할 수 있다.



#### 종류

- Simple Factory Pattern: 인터페이스는 객체 생성 로직을 숨기고 객체를 생성
- Factory Method Pattern: 인터페이스를 통해 객체를 생성하며, 서브 클래스가 객체 생성에 필요한 클래스를 선택
- Abstract Factory Pattern: 객체 생성에 필요한 클래스를 노출하지 않고 객체를 생성하는 인터페이스. 내부적으로 다른 팩토리의 객체를 생성



### 1. Simple Factory Pattern

- 여러 종류의 객체를 사용자가 직접 클래스를 호출하지 않고 생성



#### ABCMeta

- python에서 특정 클래스를 추상 클래스로 선언하는 특수 메타 클래스



##### 구현 예시

```python
from abc import ABCMeta, abstractclassmethod


# 하부 클래스에서 상속하여 사용하기 위한 추상 클래스
class OriginalClass(metaclass=ABCMeta):
    # 추상 클래스에서 상속용으로 선언하는 메서드
    @abstractclassmethod
    def do_something(self):
        pass


class SubClassA(OriginalClass):
    # 상속으로 선언된 메서드를 오버라이드
    def do_something(self):
        print("Call A")


class SubClassB(OriginalClass):
    def do_something(self):
        print("Call B")


class ClassFactory():
    # string으로 클래스 이름을 받아 해당 클래스를 생성
    def make_class(self, input_class):
        return eval(input_class)().do_something()


if __name__ == '__main__':
    class_factory = ClassFactory()
    subclass_A = class_factory.make_class('SubClassA')
    subclass_B = class_factory.make_class('SubClassB')

```

- `eval()`: string으로 값을 받아 python에서 사용하는 수식으로 변경하여 실행한 결과를 리턴
  - ex) eval('1+2') => 3
- `OriginalClass` 를 추상클래스로 선언하여 `SubClassA` 와 `SubClassB` 를 호출
- `ClassFactory` 의 `make_class` 메서드를 통해 간접적으로 클래스를 생성



> ##### 출력 결과

<img width="150" alt="스크린샷 2020-01-12 오후 6 41 01" src="https://user-images.githubusercontent.com/19590371/72216981-93765500-356b-11ea-928e-fe0d049127b9.png">

- 각 클래스의 `do_something` 을 호출



### 2. Factory Method Pattern

#### 팩토리 메서드는...

- **인터페이스를 통해 객체를 생성**하지만, 팩토리가 **아닌 서브 클래스**가 해당 객체 생성을 위해 **어떤 클래스를 호출할지 결정**
- 인스턴스화가 아닌 **상속을 통해 객체를 생성**
- 유동적이다. 심플 팩토리 메서드처럼 특정 객체가 아닌 같은 인스턴스나 서브 클래스 객체를 반환할 수 있다.
- 즉, **객체를 생성할 인터페이스를 정의**하지만, 어떤 클래스를 초기화 할지는 서브 클래스가 결정



#### 구조

- 팩토리 메서드 패턴에서 생성되는 클래스와 활용하는 클래스 역할을 구분한다.
- `Creator`: 클래스를 생성할 인터페이스를 제공하는 추상 클래스
  - `ConcreteCreator`: `Creator` 를 상속받아 생성할 클래스를 정하는 **서브 클래스**
- `Product`: 실제 생성되는 클래스들의 추상 클래스
  - `ConcreteProduct`: `Product` 를 상속받아 정의된 **실제 생성되는 클래스**



##### 프로필 생성 프로그램 예시

> ##### 생성에 대한 클래스(Product)

```python
from abc import ABCMeta, abstractmethod


# 팩터리 메서드를 통해 생성될 클래스들의 추상 클래스(Product 역할)
# 각 섹션에 대한 추상클래스
class Section(metaclass=ABCMeta):
    @abstractmethod
    def describe(self):
        pass

# Section 추상 클래스를 상속받아 각 섹션 구현
class PersonalSection(Section):
    def describe(self):
        print("Personal Section")


class AlbumSection(Section):
    def describe(self):
        print("Album Section")


class PatentSection(Section):
    def describe(self):
        print("Patent Section")


class PublicationSection(Section):
    def describe(self):
        print("Publication Section")

```

- `Section` 클래스는 실제로 생성될 클래스들의 추상 클래스
- 각 클래스는 `Section` 을 상속받아 스펙을 명시



> ##### 호출에 대한 클래스(Creator)

```python
# 클래스를 생성하는 추상 클래스(Creator 역할)
class Profile(metaclass=ABCMeta):
    def __init__(self):
        self.sections = []
        self.create_profile()
    
    @abstractmethod
    def create_profile(self):
        pass
    
    def get_sections(self):
        return self.sections
    
    def add_sections(self, section):
        self.sections.append(section)


class LinkedIn(Profile):
    def create_profile(self):
        self.add_sections(PersonalSection())
        self.add_sections(PatentSection())
        self.add_sections(PublicationSection())
        

class FaceBook(Profile):
    def create_profile(self):
        self.add_sections(PersonalSection())
        self.add_sections(AlbumSection)


if __name__ == '__main__':
    linkedin_profile = LinkedIn()
    print('Profile: ', type(linkedin_profile).__name__)
    print('Sections of profile: ', linkedin_profile.get_sections())

    facebook_profile = FaceBook()
    print('Profile: ', type(facebook_profile).__name__)
    print('Sections of profile: ', facebook_profile.get_sections())

```

- `Profile` 클래스는 클래스 호출을 담당하는 추상 클래스
- `LinkedIn` 과 `FaceBook` 클래스는 `Profile` 클래스를 상속받아 실제 **생성할 클래스를 선택**
  - 상속받은 `create_profile` 메서드를 통해 섹션(product)를 생성



> ##### 실행 결과

<img width="1220" alt="스크린샷 2020-01-12 오후 7 22 16" src="https://user-images.githubusercontent.com/19590371/72217425-dc7cd800-3570-11ea-8888-8f796d1a30d3.png">



#### 팩토리 메서드 패턴의 장점

- 유연성과 포괄성을 갖추며, 한 클래스에 종속되지 않는다.
  - 다만 인터페이스(Product)에 의존
- 객체 생성 코드와 활용 코드를 분리해 의존성이 줄어든다.



### 3. Abstract Factory Pattern

- 클래슬르 직접 호출하지 않고 **관련 객체를 생성하는 인터페이스 제공**
- **객체의 집합**을 생성
- 객체 생성 로직과 상관 없이 생성된 객체를 사용



#### 구조

- `<interface> AbstractFactory`: 사용자가 객체를 생성하기 위해 사용하는 **인터페이스**
  - `ConcreateFactory 1, 2, ...`: 인터페이스로 부터 생성된, 다른 클래스(Product)를 생성하기 위한 클래스
  - `<interface> AbstractProduct`: Product가 구현을 위해 사용하는 인터페이스
  - `<interface> AnotherAbstractProduct`: 위와 동일한 기능
  - `ConcreteProduct 1, 2, ...`: `AbstractProduct` 를 상속받아 구현된 클래스. `ConcreteFactory` 에 의해 생성



##### 피자 가게 예시

> ##### 사용 부분

```python
from abc import ABCMeta, abstractmethod


# AbstractFactory 역할을 하는 인터페이스
class PizzaFactory(metaclass=ABCMeta):
    # ConcreteFactory가 상속받을 메서드
    @abstractmethod
    def create_veg_pizza(self):
        pass

    @abstractmethod
    def create_non_veg_pizza(self):
        pass


# ConcreteFactory 역할을 하는 클래스
class IndianPizzaFactory(PizzaFactory):
    # 실제 Product를 생성하는 메서드
    def create_veg_pizza(self):
        return DeluxVeggiePizza()

    def create_non_veg_pizza(self):
        return ChickenPizza()


class USPizzaFactory(PizzaFactory):
    def create_veg_pizza(self):
        return MexicanVegPizza()

    def create_non_veg_pizza(self):
        return HamPizza()
```

- 채식, 비채식 피자를 생성하는 `PizzaFactory`
  - 클라이언트가 사용할 `AbstractFactory` 역할을 맡는다.
- 피자를 생성을 실제로 구현한 `Indian, USPizzaFactory`
  - `ConcreteFactory` 역할로 실제 `Product` 를 생상한다.



> ##### 생성 부분

```python
# (Another)AbstractProduct 역할을 하는 인터페이스
# 실제 Product가 상속하여 사용
class VegPizza(metaclass=ABCMeta):
    # Product가 상속할 메서드
    @abstractmethod
    def prepare(self, VegPizza):
        pass


class NonVegPizza(metaclass=ABCMeta):
    @abstractmethod
    def serve(self, VegPizza):
        pass


# 실제 생성되는 Product
class DeluxVeggiePizza(VegPizza):
    def prepare(self):
        print("Prepare Veggie: ", type(self).__name__)


class ChickenPizza(NonVegPizza):
    def serve(self, VegPizza):
        print(type(self).__name__, "is served with chicken", type(VegPizza).__name__)


class MexicanVegPizza(VegPizza):
    def prepare(self):
        print("Prepare Veggie: ", type(self).__name__)


class HamPizza(NonVegPizza):
    def serve(self, VegPizza):
        print(type(self).__name__, "is served with Ham", type(VegPizza).__name__)


class PizzaStore:
    def __init__(self):
        pass

    def make_pizzas(self):
        for factory in [IndianPizzaFactory(), USPizzaFactory()]:
            self.factory = factory
            self.non_veg_pizza = self.factory.create_non_veg_pizza()
            self.veg_pizza = self.factory.create_veg_pizza()
            self.veg_pizza.prepare()
            self.non_veg_pizza.serve(self.veg_pizza)


pizza = PizzaStore()
pizza.make_pizzas()
```

- `Product` 가 상속하는 `VegPizza`, `NonVegPizza`
  - 이 예시에서 `NonVegPizza` 는 `VegPizza` 를 사용하여 생성



> ##### 실행 결과

<img width="383" alt="스크린샷 2020-01-13 오후 11 14 23" src="https://user-images.githubusercontent.com/19590371/72262534-78ced980-365a-11ea-89d1-41c81541ab3a.png">



#### 팩토리 메서드 vs 추상 팩토리 메서드

| 팩토리 메서드                                           | 추상 팩토리 메서드                                           |
| ------------------------------------------------------- | ------------------------------------------------------------ |
| 객체 생성에 필요한 메서드가 노출된다                    | **객체 집단**을 생성하기 위해 한 개 이상의 팩토리 메서드가 필요 |
| 어떤 객체를 생성할지를 결정할 상속과 서브 클래스가 필요 | 다르 클래스 객체를 생성하기 위한 **컴포지션** 사용           |
| 한 개의 객체를 생성                                     | 객체 집단을 생성                                             |



### 4. 정리

- Simple Factory: **런타임**에 클라이언트가 인자로 넘긴 객체형에 대한 인스턴스 생성
- Factory Method: 인터페이스를 통해 객체를 생성하지만, **실제 생성은 서브클래스**가 담당
- Abstract Factory Method: `Concrete Class` 를 명시하지 않고, 관련 객체의 **집단**을 생성