## Singleton Pattern

- 글로벌하게 접근 가능한 **한 개의 객체만을 생성**하는 패턴



#### 사용 이유

- 로깅, DB작업, 프린터 스풀러 등 어플리케이션 리소스에 대한 동시 요청 충돌을 막기 위해 한개의 인스턴스만 생성
  - ex) 일관성을 위해 DB 접근 객체를 하나만 생성
- 클래스에 대한 단일 전역 객체 제공
- 공유된 리소스에 대한 동시 제어



### 1. 구현 방법

- Constructor를 private으로 선언
- 객체를 초기화 하는 static함수, 객체를 return하는 static함수 구현



#### Python에서 구현

```python
class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
    	    cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
      
s = Singleton()
print("Object created", s)

s1 = Singleton()
print("Object created", s1)
```

- `super(Singleton, cls)`: `Singleton` 클래스 자신의 부모에 접근합니다ㅣ
- `hasattr`을 통해 클래스 자체에서 `instance`를 갖고 있는지 확인한 후 없으면 `instance` 객체를 생성합니다.
- `cls`: 클래스 그 자체를 의미하는 변수



> ##### 실행 결과

<img width="404" alt="스크린샷 2019-12-17 오후 10 29 43" src="https://user-images.githubusercontent.com/19590371/70999453-cf5cfc80-211c-11ea-91dd-a32fb09d6ad4.png">

- 매 요청마다 같은 객체를 반환



> #### \__init__과 self를 사용한다면

```python
class Singleton(object):
    def __init__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(Singleton, self).__init__()
        return self.instance
      
s = Singleton()
print("Object created", s)

s1 = Singleton()
print("Object created", s1)
```



> ##### 실행 결과

<img width="406" alt="스크린샷 2019-12-17 오후 10 29 21" src="https://user-images.githubusercontent.com/19590371/70999451-cf5cfc80-211c-11ea-8a3a-af4a354d4629.png">

- 매 요청마다 다른 객체를 반환



### 2. Lazy Initialization

- 클래스를 생성하면서 필요하지 않은 시점에 객체가 미리 만들어 질 수 있다.
- 객체가 꼭 필요한 시점에만 객체를 생성
- 클래스를 초기화 한 후 **함수를 통해** 객체를 생성  



#### Python에서 구현

```python
class Singleton:
    __instance = None
    def __init__(self):
        if not Singleton.__instance:
            print("__init__ method called...")
        else:
            print("Instance already created:", self.getInstance())
    
    @classmethod
    def getInstance(cls):
        if not cls.__instance:
            cls.__instance = Singleton()
        return cls.__instance

s = Singleton() # 클래스 초기화, 객체 생성 X
Singleton.getInstance() # 객체 생성
s1 = Singleton().getInstance() # getInstance를 통해 싱글턴 객체에 접근
print(s1)

s2 = Singleton()
print(s2)
```

- `__instance`: 클래스 전역 객체
- `classmethod` 인 `getInstance`를 통해 객체 생성, 접근



>##### 실행 결과

<img width="490" alt="스크린샷 2019-12-18 오후 10 55 25" src="https://user-images.githubusercontent.com/19590371/71091951-89219f00-21e9-11ea-8358-63828ed170de.png">



##### s2에 대해...

- 위 코드에서 `getInstance()` 를 통해 반환 받은 객체의 주소는 0x103cf8208 입니다.
- s1을 print하면 동일한 주소에 대한 객체가 반환됩니다.
- 반면 s2는 `Singleton` 생성자를 통해 반환받은 객체를 쥐고 있으며 s1이 담고 있는 객체의 주소와는 다릅니다.
- s2는 정확하게 말하면 `getInstance` 를 통해 생성된 즉, **싱글턴 패턴을 통해 생성된 객체가 아닌** 이름이`Singleton` 인 클래스의 **생성자를 통해 생성된 객체**입니다.
- 두 객체는 완전히 다른 객체이며, 싱글턴 패턴을 통해 생성된 객체에 접근하기 위해선 `getInstance` 메서드를 통해 접근해야 합니다.



#### Java에서 구현

```java
 public class Singleton {
		private static Singleton instance = null;
		
  	private Singleton(){} // 외부에서 생성자에 접근 불가능

		public static Singleton getInstance(){ // Singleton instance 반환
				if(instance == null){
						instance = new Singleton();
				}

				return instance;
		}

    public void printInstance(){
      	System.out.println("Singletone instance");
    }

    public static void main(String[] args) {
        Singletone singleton = Singletone.getInstance();
      	singletone.printInstance();
    }
}
```

- 생성자에 접근하지 못하게 한 후 `getInstance`를 통해서만 객체에 접근
- `static` 이기 때문에 매 번 같은 객체를 반환



#### Python vs Java

- python은 클래스 자체를 제어하는 것이 가능하므로 생성자를 실행한 후 `classmethod`를 통해 전역 객체 생성
- Java는 `static` 메서드를 통해 전역 객체를 생성



#### Module Singleton

- 파이썬에서 import방식에 의해 모든 모듈은 싱글톤입니다.

##### 작동 방식

1. Python은 모듈이 import되었는지 확인
2. 됐다면, 해당 객체를 반환하고 아니면 import하여 instance화
3. 모듈은 import하는 순간 초기화. 하지만, 같은 모듈을 import하면 초기화 하지 않는다.



### 3. Monostate Singleton Pattern

- 모든 객체가 같은 상태를 공유하는 패턴
- 한 객체의 데이터의 유일성을 보장할 수 있는 방법
- 객체를 파생해도 동일한 상태를 공유



#### 단점

- 객체가 사용되지 않더라도 메모리 공간을 차지한다
- 생성과 소멸이 잦으며, 많은 비용이 소모된다.



#### 구현 예시

```python
class Borg:
    __shared_state = {"1": "2"}
    
    def __init__(self):
        self.x = 1
        self.__dict__ = {}

b1 = Borg()
b2 = Borg()

b2.x = 4

print("b1 is :", b1)
print("b2 is :", b2)

print("b1 x: ", b1.x)
print("b2 x: ", b2.x)

print("b1 dict: ", b1.__dict__)
print("b2 dict: ", b2.__dict__)
```

- `__dict__`: 클래스 내부 속성 변수를 dictionary 관리하는 변수
  - `self.x` 를 선언해도 `self.__dict__` 를 사용하면 속성변수 `x` 에 접근할 수 없게된다.
  - 이후 b2.x = 4 를 통해 x 변수를 dictionary로 관리
- 해당 코드에서 `__shared_state` 에 있는 데이터를 dictionary로 관리하게 되고 모든 인스턴스에서 공유하게 된다.



>##### 실행 결과

<img width="347" alt="스크린샷 2019-12-28 오후 4 31 37" src="https://user-images.githubusercontent.com/19590371/71540545-9419c380-298f-11ea-9914-d03a8d6e8af9.png">



#### \__new__를 사용한 구현

```python
class Book(object):
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(Book, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        print(obj)

        return obj

book1 = Book() # 다른 객체이지만 상태를 공유한다.
book2 = Book()

book1.x = 1
book2.y = 2

print(book1.__dict__)
print(book2.__dict__)
```



> ##### 실행 결과

<img width="284" alt="스크린샷 2020-01-02 오후 10 42 16" src="https://user-images.githubusercontent.com/19590371/71669769-33382400-2db1-11ea-9c4b-7b9c1dad8809.png">





### 4. Singleton and Meta class

#### Meta class

- 클래스의 클래스
- 클래스 그 자체는 메타 클래스의 인스턴스
- 이미 정의된 클래스를 통해 새로운 형식의 클래스 생성 가능
  - 상속과 유사한 기능처럼 보인다



#### Meta class vs Inheritance

- 보통 메타 클래스는 OOP의 제약을 벗어난 구현을 위해 사용
- 한 객체가 메타 클래스로 부터 받은 method를 호출해도 메타 클래스의 해당 메서드를 찾지 않는다.
  - 다만 객체가 생성될 시에 메타 클래스가 미리 생성
  - python이 인터프리터를 사용하기에 가능
- 상속과 다르게 부모-자식관계로 묶여 있지 않으며, 서로 다른 객체
- OOP의 제약을 벗어난 극도로 dynamic한 프로그래밍 시에 사용 추천
  - [Stack overflow 답변](https://stackoverflow.com/questions/17801344/understanding-metaclass-and-inheritance-in-python)



> ##### 예시

<img width="127" alt="스크린샷 2020-01-02 오후 10 57 35" src="https://user-images.githubusercontent.com/19590371/71670480-4b10a780-2db3-11ea-8821-516de82a6914.png">

- python에서 모든 것은 객체이다
- type 클래스가 int 클래스의 메타클래스
  - int가 type을 재정의



#### python에서 클래스

- 기본적으로 python에서 `class` 를 사용해 정의한 클래스는 **클래스 이면서 객체**이다
- **클래스 그 자체**이기도 하지만 **동시에 객체**이기도 하다



> ##### type을 통해 클래스의 자료형을 확인

```python
class Car:
    pass

print(type(Car))

# 출력 결과

<class 'type'>
```

- python에서 모든 클래스는 클래스 이며 `type`이라는 **클래스의 객체**이기도 하다



#### type

- `type` 은 python에서 자료형을 확인하는 함수이지만, 또 다른 기능으로 **클래스를 생성하는 기능이 있다**.
- 인자를 보면 type(`name`, `bases`, `dict`)의 인자를 받는다
  - name: 클래스 명
  - base: 베이스 클래스
  - dict: 속성값
- 인자로 클래스를 이루는 정의를 받아 클래스를 반환
  - 그리고 이 클래스는 객체가 되기도 한다
- class Car 라는 코드는 사실상 `type` 이 실행되어 **클래스(이면서 객체)를 반환**하는 과정을 거친다.
- 메타 클래스는 클래스의 클래스 이며 **클래스를 생성하는 클래스**이다.
  - 즉, 메타 클래스는 **클래스 생성을 제어**할 수 있다.
- `type` 은 메타 클래스이며, **클래스를 생성하는 메타클래스**이다.



##### type을 통한 클래스 및 인스턴스 생성

```python
# type을 통해 Wing 클래스를 생성하고 A에 저장

A = type("Wing", (), {"x": 1})
print(A)
print(A.__dict__)

# A를 통해 Wing class의 인스턴스를 생성 후 a1에저장, 값을 확인

a1 = A()
print(a1.x)
```



> ##### 출력 결과

<img width="567" alt="스크린샷 2020-01-02 오후 11 22 21" src="https://user-images.githubusercontent.com/19590371/71671623-da6b8a00-2db6-11ea-965c-24da63d784e7.png">



#### 그래서...

- 메타 클래스를 통해 클래스와 객체 생성을 제어할 수 있으며, 이는 **싱글톤을 생성**하는 용도로 사용할 수 있다는 것과 같다



#### 메타 클래스를 통한 싱글턴 생성

```python
class MetaSingleton(type):
    _instances = {}
		
    # 클래스를 함수처럼 사용할 때 호출되는 메서드
    # ex) a = A(), a()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class Book(metaclass=MetaSingleton):
    pass


book1 = Book()
book2 = Book()

print(book1)
print(book2)
```



> ##### 출력 결과

<img width="272" alt="스크린샷 2020-01-02 오후 11 43 24" src="https://user-images.githubusercontent.com/19590371/71672561-b1002d80-2db9-11ea-8a7e-e55dd5947b80.png">



### 5. Examples

#### 데이터베이스

- 여러 서비스가 한 개의 DB를 공유하는 구조
- 안정된 서비스를 위해
  - DB의 일관성을 보존해야 하며, **연산간 충돌**이 없어야 한다.
  - 다수의 DB 연산을 처리하려면 메모리와 CPU를 효율적으로 사용해야 한다.



> ##### 싱글턴을 통해 하나의 DB 접속 객체 생성

```python
import sqlite3

# 객체를 싱글턴으로 만드는 역할

class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        
        return cls._instances[cls]


# MetaSingleton으로 인해 1개의 Database 객체만 생성

class Database(metaclass=MetaSingleton):
    connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db.sqlite3")
            self.cursorobj = self.connection.cursor()

        return self.cursorobj


db1 = Database().connect()
db2 = Database().connect()

print(db1)
print(db2)

```

1. `MetaSingleton` 메타 클래스에 의해 `Database` 객체는 싱글턴으로 생성
2. 웹 앱이 DB 요청을 할 때 마다 `Database` 클래스 객체를 한개만 생성하여 DB 동기화를 보장
   - 리소스를 하나만 사용하여 CPU, 메모리 효율적 사용



#### 인프라 상태 확인

```python
class StatusCheck:
    _instance = None
    
    # 싱글턴으로 StatueCheck 객체 생성
    # 클래스 메서드인 __new__를 사용
    
    def __new__(cls, *args, **kwargs):
        if not StatusCheck._instance:
            StatusCheck._instance = super(StatusCheck, cls).__new__(cls, *args, **kwargs)

        return StatusCheck._instance

    # 싱글턴에서 공동으로 공유하는 자원
    
    def __init__(self):
        self._servers = []
		
    def addServer(self):
        self._servers.append("Server 1")
        self._servers.append("Server 2")
        self._servers.append("Server 3")
        self._servers.append("Server 4")

    def changeServer(self):
        self._servers.pop()
        self._servers.append("Server 5")

# 동일한 두 객체

status_check1 = StatusCheck()
status_check2 = StatusCheck()

status_check1.addServer()
print("Schedule statue check for servers (1)")

for i in range(4):
    print("Checking ", status_check1._servers[i])

status_check2.changeServer()
print("Schedule statue check for servers (2)")

for i in range(4):
    print("Checking ", status_check2._servers[i])

```



> ##### 실행 결과

<img width="277" alt="스크린샷 2020-01-07 오후 11 42 35" src="https://user-images.githubusercontent.com/19590371/71903443-7296b400-31a7-11ea-903d-25de6c2558c5.png">

- 동일한 객체 `status_check1`, `status_check2` 에서 `_servers` 배열을 조작



### 6. 정리

#### 싱글턴의 단점

- 같은 객체에 여러 참조자가 있을 수 있다.
- 전역 객체에 종속적인 클래스간 관계가 복잡하며, 전역 객체 수정이 다른 클래스에 영향을 미칠 수 있다.



#### 싱글턴을 사용하는 상황

- 어플리케이션에서 풀, 캐시, 설정 등 한 개의 객체만 필요한 경우에 생성하여 사용
- 글로벌 액세스를 제공해야 하는 경우
- **클래스 객체가 한 개만 필요한 경우**에 사용

