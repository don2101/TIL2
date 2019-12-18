class Singleton(object):
    def __new__(cls):
        print(cls)
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance
      
    # def __init__(self):
    #     print(self)

s = Singleton()
print("Object created", s)

s1 = Singleton()
print("Object created", s1)