# 각 컴퓨터의 상태에 따라 허용된 상태 변화를 정의 하는 State 역할의 인터페이스
# 인터페이스에서 ConcreteState를 제어
class ComputerState(object):
    name = None
    allowed = []

    def switch(self, state):
        if state.name in self.allowed:
            print('switch', self, ' to new state ', state.name)
            self.__class__ = state
        else:
            print(self, ' to new state ', state.name, ' is not possible')

    def __str__(self):
        return self.name
    

# ConcreteState 역할을 하는 클래스
# name: 현재 상태, allowed: 현재 상태에서 변화할 수 있는 상태
class Off(ComputerState):
    name = "off"
    allowed = ["on"]

    
class On(ComputerState):
    name = "on"
    allowed = ["off", "suspend", "hibernate"]

    
class Suspend(ComputerState):
    name = "suspend"
    allowed = ["on"]

    
class Hibernate(ComputerState):
    name = "hibernate"
    allowed = ["on"]


# Context 역할을 하는 클래스
class Computer(object):
    def __init__(self):
        self.state = Off()

    def change(self, state):
        self.state.switch(state)


# 클래스 자체를 삽입하여 
computer = Computer()
computer.change(On)
computer.change(Off)
computer.change(On)
computer.change(Suspend)
computer.change(Hibernate)
computer.change(Off)
computer.change(On)
computer.change(Suspend)
computer.change(Hibernate)
