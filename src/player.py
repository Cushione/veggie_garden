from .events import Events
from .storage import Storage
from .fertiliser import Fertiliser

class Player():
    def __init__(self, money=20):
        self.money = money
        self.events = Events()
        self.storage = Storage([0,0,0,0,0])
        self.fertiliser = Fertiliser(0)
        #self.fields
        #self.store
