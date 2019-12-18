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
