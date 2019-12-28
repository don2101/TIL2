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



#### Monostate Singleton Pattern

- 모든 객체가 같은 상태를 공유하는 패턴



> #### 구현 예시

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



> #### 출력 결과

<img width="347" alt="스크린샷 2019-12-28 오후 4 31 37" src="https://user-images.githubusercontent.com/19590371/71540545-9419c380-298f-11ea-9914-d03a8d6e8af9.png">





