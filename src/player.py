from .events import Events
from .storage import Storage

class Player():
    def __init__(self, money=20):
        self.money = money
        self.events = Events()
        self.storage = Storage([0,0,0,0,0])
        #self.fertilizer
        #self.fields
        #self.store
