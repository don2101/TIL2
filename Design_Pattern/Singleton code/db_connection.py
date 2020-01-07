import sqlite3

# 객체를 싱글턴으로 만드는 역할
class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        
        return cls._instances[cls]


# MetaSingleton으로 인해 1개의 Database 객체만 생성
class Database(metaclass=MetaSingleton):
    connection = None

    def connect(self):
        if self.connection is None:
            self.connection = sqlite3.connect("db.sqlite3")
            self.cursorobj = self.connection.cursor()

        return self.cursorobj


db1 = Database().connect()
db2 = Database().connect()

print(db1)
print(db2)

