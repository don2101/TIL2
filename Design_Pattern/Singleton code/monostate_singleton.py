class Borg:
    __shared_state = {"1": "2"}
    
    def __init__(self):
        self.x = 1
        self.__dict__ = self.__shared_state

b1 = Borg()
b2 = Borg()

b2.x = 4

print("b1 is :", b1)
print("b2 is :", b2)

print("b1 x: ", b1.x)
print("b2 x: ", b2.x)

print("b1 dict: ", b1.__dict__)
print("b2 dict: ", b2.__dict__)
