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