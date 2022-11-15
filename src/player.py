from .events import Events

class Player():
    def __init__(self, money=20):
        self.money = money
        self.events = Events()
        #self.storage
        #self.fertilizer
        #self.fields
        #self.store
