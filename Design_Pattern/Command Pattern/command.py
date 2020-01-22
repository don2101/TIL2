from abc import ABCMeta, abstractmethod


# 구현될 Command. 실제 수행될 행동에 대한 인터페이스 제공
class Command(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


# 구현된 Command. 각 기능에 따라 Recevier를 받아 저장하고, 해당 기능을 수행을 캡슐화
class ConcreteCommand1(Command):
    def __init__(self, flasher):
        self.flasher = flasher

    def execute(self):
        self.flasher.light_on()


class ConcreteCommand2(Command):
    def __init__(self, watergun):
        self.watergun = watergun
        
    def execute(self):
        self.watergun.shoot_water()       


# Receiver 역할을 하는 Flasher와 Watergun. 실제 기능을 수행
class Flasher:
    def light_on(self):
        print("Light on")


class Watergun:
    def shoot_water(self):
        print("Shoot water")


class Invoker:
    def set_command(self, command):
        self.command = command

    def execute(self):
        self.command.execute()


if __name__ == '__main__':
    flasher = Flasher()
    watergun = Watergun()

    command1 = ConcreteCommand1(flasher)
    command2 = ConcreteCommand2(watergun)

    invoker = Invoker()
    invoker.set_command(command1)
    invoker.execute()
    invoker.set_command(command2)
    invoker.execute()
    invoker.set_command(command1)
    invoker.execute()
