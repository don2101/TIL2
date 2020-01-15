from abc import ABCMeta, abstractmethod


# Object 역할
# Bank와 DebitCard가 구현하는 인터페이스
class Payment(metaclass=ABCMeta):
    @abstractmethod
    def do_pay(self):
        pass


# Real Object 역할
class Bank(Payment):
    def __init__(self):
        self.card = None
        self.account = None

    def __get_account(self):
        self.account = self.card

        return self.account

    def __check_money(self):
        print("Check", self.__get_account(), "has enough money")

        return True

    def set_card(self, card):
        self.card = card

    def do_pay(self):
        if self.__check_money():
            print("Bank made payment")
            
            return True
        else:
            print("At bank Not enough money")        

            return False


# Bank를 대신해 결제를 대신하는 Proxy
class DebitCard(Payment):
    def __init__(self):
        self.bank = Bank()

    # Bank에 직접 접근하지 않고 Bank를 대신해 결제 진행
    def do_pay(self):
        card_number = 12345
        self.bank.set_card(card_number)

        return self.bank.do_pay()


class Client(object):
    def __init__(self):
        print("Wanna buy a shirt")
        self.debit_card = DebitCard()
        self.is_purchasable = None

    def make_payment(self):
        self.is_purchasable = self.debit_card.do_pay()

    def __del__(self):
        if self.is_purchasable:
            print("Buy a shirt")
        else:
            print("Not enough money")


client = Client()
client.make_payment()