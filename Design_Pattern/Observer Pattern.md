## Observer Pattern

### 1. Behavioral Pattern

- 역할(객체의 행동)에 집중
- 객체간 상호작용 하지만 느슨한 결합을 유지한다.



### 2. Observer Pattern

- 객체(Subject)가 **자식(Observer)의 리스트**를 갖고 있다.

- `Subject`가 `Observer`에 **정의 된 메소드를 호출**하고, `Observer`에게 이를 알린다.

  - ex) 분산형 어플리케이션의 서비스, 종속된 서비스가 코어 서비스의 상태를 참고하는 형태,

    `Publish` - `Subscribe` 구조, 브로드캐스트



#### Publish - Subscribe 구조

1. 독자의 특정 title에 대한 구독 신청
2. 작가가 글을 등록하면, 구독자에게 알림(이메일) 송신

- 작가는 구독자 또는 `Observer`의 목록을 유지하는 `Subject`이며, 이벤트 발생시 알림을 보낸다.



#### 목적

- 객체간 1:N 관계를 형성하여 종속객체에 **객체의 상태를 자동으로 알린다**.
- `Subject` 핵심 부분 캡슐화
- 분산 시스템에서 **이벤트 서비스 구현**
  - 뉴스 에이전시, 주식 시장



### 3. 구조

![Observer](https://user-images.githubusercontent.com/19590371/72730899-cbb60d00-3bd5-11ea-9e71-481e638c41ab.png)

- `Subject`: 여러 Observer들을 관리하고, 알리는 객체. 상태 변화(이벤트)가 발생하면, `Observer` 인터페이스를 통해 `ConcreteObserver` 에게 알림 발송
- `Observer`: `Subject` 를 감시하기 위한 **인터페이스 제공**
- `ConcreteObserver`: `Subject` 의 상태를 저장. `Observer` 를 통해 `Subject` 에 자신을 등록



### 4. 구현 예시

#### 옵저버 패턴 구현

```python
class Subject:
    def __init__(self):
        self.__observers = []

    def register(self, observer):
        self.__observers.append(observer)

    def notifyAll(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)


class Observer1:
    def __init__(self, subject):
        subject.register(self)

    def notify(self, subject, *args):
        print(type(self).__name__, 'Got ', args, 'From', subject)


class Observer2:
    def __init__(self, subject):
        subject.register(self)

    def notify(self, subject, *args):
        print(type(self).__name__, 'Got ', args, 'From', subject)


subject = Subject()
observer1 = Observer1(subject)
observer2 = Observer2(subject)

subject.notifyAll('notification')
```



> ##### 실행 결과

<img width="555" alt="스크린샷 2020-01-20 오후 10 50 19" src="https://user-images.githubusercontent.com/19590371/72731607-5c411d00-3bd7-11ea-82c6-b8fbfe514b6a.png">



#### 뉴스 에이전시 구현 예시

- 여러 곳에서 뉴스를 모아 구독자에게 전달



##### 뉴스 에이전시

```python
# Subject 역할을 하는 NewsPublisher
class NewsPublisher:
    def __init__(self):
        self.__subscribers = []
        self.__latest_news = None

    # 구독자에게 제공하는 구독 메서드
    def subscribe(self, subscriber):
        self.__subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        self.__subscribers.pop(subscriber)

    def get_subscribers(self):
        return [type(subscriber) for subscriber in self.__subscribers]

    # 구독자의 update 메서드를 통해 구독자에게 알림을 전송
    def notifySubscribers(self):
        for subscriber in self.__subscribers:
            subscriber.update()

    def add_news(self, news):
        self.__latest_news = news

    def get_new(self):
        return self.__latest_news

```



##### 구독자 부분

```python
from abc import ABCMeta, abstractmethod


# Observer가 구현할 메서드를 정의한 Observer
class Subscriber(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        pass


# Observer를 구현한 ConcreteObserver
class SMSSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    # Subject에게 제공하는 update 메서드
    def update(self):
        print(type(self).__name__, self.publisher.get_news())


class EmailSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.get_news())


class VideoSubscriber:
    def __init__(self, publisher):
        self.publisher = publisher
        self.publisher.attach(self)

    def update(self):
        print(type(self).__name__, self.publisher.get_news())

        
if __name__ == '__main__':
    news_publisher = NewsPublisher()

    for Subscribers in [SMSSubscriber, EmailSubscriber, VideoSubscriber]:
        Subscribers(news_publisher)
    
    news_publisher.add_news("Big News")
    news_publisher.add_news("Big news2")
```



> ##### 출력 결과

<img width="206" alt="스크린샷 2020-01-20 오후 11 30 00" src="https://user-images.githubusercontent.com/19590371/72734315-ca3c1300-3bdc-11ea-905b-4d6c84762a72.png">



