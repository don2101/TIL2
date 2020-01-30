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