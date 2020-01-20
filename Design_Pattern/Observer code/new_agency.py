from abc import ABCMeta, abstractmethod

# Subject 역할을 하는 NewsPublisher
class NewsPublisher:
    def __init__(self):
        self.__subscribers = []
        self.__latest_news = None

    # 구독자에게 제공하는 구독 메서드
    def subscribe(self, subscriber):
        self.__subscribers.append(subscriber)

    # 구독자의 update 메서드를 통해 구독자에게 알림을 전송
    def notifySubscribers(self):
        for subscriber in self.__subscribers:
            subscriber.update()

    def add_news(self, news):
        self.__latest_news = news
        self.notifySubscribers()

    def get_news(self):
        return self.__latest_news


# Observer가 구현할 메서드를 정의한 Observer
class Subscriber(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        pass


# Observer를 구현한 ConcreteObserver
class SMSSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.subscribe(self)

    # Subject에게 제공하는 update 메서드
    def update(self):
        print(type(self).__name__, self.publisher.get_news())


class EmailSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.subscribe(self)

    def update(self):
        print(type(self).__name__, self.publisher.get_news())


class VideoSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.subscribe(self)

    def update(self):
        print(type(self).__name__, self.publisher.get_news())


if __name__ == '__main__':
    news_publisher = NewsPublisher()

    for Subscribers in [SMSSubscriber, EmailSubscriber, VideoSubscriber]:
        Subscribers(news_publisher)
    
    news_publisher.add_news("Big News")
    news_publisher.add_news("Big news2")