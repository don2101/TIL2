from abc import ABCMeta, abstractmethod


class State(metaclass=ABCMeta):
    @abstractmethod
    def Handle(self):
        pass


class ConcreteStateA(State):
    def Handle(self):
        print("Call State A")


class ConcreteStateB(State):
    def Handle(self):
        print("Call State B")


# state 를 저장하고 상황에 따라 다른 함수 호출
class Context(State):
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def Handle(self):
        self.state.Handle()


context = Context()
state_a = ConcreteStateA()
state_b = ConcreteStateB()

context.set_state(state_a)
context.Handle()
context.set_state(state_b)
context.Handle()
