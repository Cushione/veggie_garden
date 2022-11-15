from .events import Events
from .storage import Storage
from .fertiliser import Fertiliser
from .field import Field
from .store import Store
from .utils import valid_number_input


class Player():
    def __init__(self, money=20):
        self.money = money
        self.events = Events()
        self.storage = Storage([0, 0, 0, 0, 0])
        self.fertiliser = Fertiliser(0)
        self.fields = [Field(None, 0, self.storage)]
        self.store = Store()
    def prepare_next_season(self):
        while True:
            print("1: Open Storage")
            print("2: Fertiliser")
            print("3: Visit Store")
            print("4: Go to Fields")
            print("5: Start season")
            print("0: Save and Exit")
            user_input = valid_number_input("What would you like to do next?: ", 0, 5)
            
            if user_input == 1:
                # TODO: Open Storage
            elif user_input == 2:
                # TODO: Open Fertiliser
            elif user_input == 3:
                self.store.buy_seeds(self)
            elif user_input == 4:
                # TODO: Open Fields
            elif user_input == 5:
                # TODO: Start season
            else:
                # TODO: Save Game and show main screen

