from .events import Events
from .storage import Storage
from .fertiliser import Fertiliser
from .field import Field

class Player():
    def __init__(self, money=20):
        self.money = money
        self.events = Events()
        self.storage = Storage([0,0,0,0,0])
        self.fertiliser = Fertiliser(0)
        self.fields = [Field(None, 0 , self.storage)]
        #self.store
