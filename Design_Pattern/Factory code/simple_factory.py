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


