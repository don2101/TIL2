class EventManager(object):
    def __init__(self):
        print("Arrange wedding...")

    def arrange(self):
        self.hotelier = Hotelier()
        self.hotelier.book_hotel()

        self.florist = Florist()
        self.florist.set_flower()

        self.caterer = Caterer()
        self.caterer.set_foods()

        self.musician = Musician()
        self.musician.play_music()


class Hotelier(object):
    def __init__(self):
        print("Booking hotel...")

    def book_hotel(self):
        print("Registered the booking")
    

class Florist(object):
    def __init__(self):
        print("Preparing flowers...")

    def set_flower(self):
        print("Prepared flowers")


class Caterer(object):
    def __init__(self):
        print("Preparing foods...")

    def set_foods(self):
        print("Prepared foods")


class Musician(object):
    def __init__(self):
        print("Preparing for music...")

    def play_music(self):
        print("Played music")


class Client(object):
    def __init__(self):
        print("Decide EventManager")
        self.event_manager = EventManager()

    def ask_wedding_arrange(self):
        self.event_manager.arrange()


client = Client()
client.ask_wedding_arrange()