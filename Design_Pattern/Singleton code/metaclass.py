class Car:
    pass

print(type(Car))

type


# A에 Wing 클래스를 저장
A = type("Wing", (), {"x": 1})
print(A)
print(A.__dict__)

# a1으로 A객체의 인스턴스를 생성 후 값을 확인
a1 = A()
print(a1.x)


class MetaSingleton(type):
    _instances = {}

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