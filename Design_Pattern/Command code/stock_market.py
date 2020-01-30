from abc import ABCMeta, abstractmethod


# Command 역할을 하는 Order. 메서드 인터페이스를 제공
class Order(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


# ConcreteCommand 역할을 하는 Buy/SellStockOrder
# 수행할 기능을 캡슐화 하여 저장
# Receiver를 저장하고 기능 수행을 Receiver에게 맡긴다
class BuyStockOrder(Order):
    def __init__(self, stock):
        self.stock = stock

    def execute(self):
        self.stock.buy()


class SellStockOrder(Order):
    def __init__(self, stock):
        self.stock = stock
    
    def execute(self):
        self.stock.sell()


# Receiver 역할을 하는 StockTrade. 실제 기능을 수행
class StockTrade:
    def buy(self):
        print("Buy stocks")

    def sell(self):
        print("Sell stocks")


# Invoker 역할을 수행하는 Agent
# 유저의 요청을 큐에 저장한 뒤 실행하고 제거
class Agent:
    def __init__(self):
        self.__order_queue = []

    def add_order(self, order):
        self.__order_queue.append(order)
        order.execute()
        self.__order_queue.pop()


if __name__ == '__main__':
    stock = StockTrade()
    buy_stock = BuyStockOrder(stock)
    sell_stock = SellStockOrder(stock)

    agent = Agent()
    agent.add_order(buy_stock)
    agent.add_order(sell_stock)
    agent.add_order(buy_stock)
    agent.add_order(sell_stock)
    