class Book(object):
    _shared_state = {}

    def __new__(cls, *args, **kwargs):
        obj = super(Book, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        print(obj)

        return obj

book1 = Book()
book2 = Book()

book1.x = 1
book2.y = 2

print(book1.__dict__)
print(book2.__dict__)

