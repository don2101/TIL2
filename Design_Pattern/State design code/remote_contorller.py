from abc import ABCMeta, abstractmethod


class TVState(metaclass=ABCMeta):
    @abstractmethod
    def press_button(self):
        pass


class TVoff(TVState):
    def press_button(self):
        print("Turn on TV")


class TVon(TVState):
    def press_button(self):
        print("Turn off TV")


class RemoteController(TVState):
    def __init__(self):
        self.state = None

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def press_button(self):
        self.state.press_button()


remote_controller = RemoteController()

on = TVon()
off = TVoff()

remote_controller.set_state(on)
remote_controller.press_button()
remote_controller.set_state(off)
remote_controller.press_button()
