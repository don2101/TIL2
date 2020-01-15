# 객체 역할을 하는 배우
class Actor(object):
    def __init__(self):
        self.isBusy = False

    def acting(self):
        self.isBusy = True
        print(type(self).__name__, "is busy")


    def available(self):
        self.isBusy = False
        print(type(self).__name__, "is free")

    def get_status(self):
        return self.isBusy


# 배우에 대한 대리 자
# 배우에 대한 접근 제어 및 상태 전달
class Agent(object):
    def __init__(self):
        pass

    def work(self, actor):
        self.actor = Actor()

        if self.actor.get_status():
            self.actor.acting()

        else:
            self.actor.available()


if __name__ == '__main__':
    agent = Agent()
    agent.work()
    