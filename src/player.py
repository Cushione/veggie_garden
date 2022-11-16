from .events import Events
from .storage import Storage
from .fertiliser import Fertiliser
from .field import Field, Garden
from .store import Store
from .utils import valid_number_input, press_enter, MONTHS
import time


class Player():
    def __init__(self, money=20, month=0):
        self.money = money
        self.month = month
        self.events = Events()
        self.storage = Storage([0, 0, 0, 0, 0])
        self.fertiliser = Fertiliser(0)
        self.garden = Garden([[None, 0]], self.storage)
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
                self.storage.display_storage_menu()
            elif user_input == 2:
                self.fertiliser.display_fertiliser_menu(self)
            elif user_input == 3:
                self.store.buy_seeds(self)
            elif user_input == 4:
                self.garden.display_field_menu(self)
            elif user_input == 5:
                self.work_season()
            else:
                # TODO: Save Game
                return False

            if self.month == 60:
                return True

    def work_season(self):
        for month in range(6):
            print(f"--- {MONTHS[month]} ---")
            time.sleep(0.5)
            self.month += 1
            if not any([field.is_filled() for field in self.garden.fields]):
                print("All fields are empty.")
                time.sleep(1)
                continue
            for index, field in enumerate(self.garden.fields):
                if not field.is_filled():
                    continue
                print(f"Tending to field {index + 1}")
                time.sleep(0.5)
                field.tend(self.month)
                time.sleep(1)
        
        print(f"\n--- End of Year {int(self.month / 6)} ---\n")
        input("Press Enter to see your profits.")
        self.season_overview()
        
        for field in self.garden.fields:
            self.money += field.seasonal_harvest
            field.plow()

    def season_overview(self):
        event = self.events.get_random_event()
        if event is not None:
            print(event.description)
            event.adjust_harvest(self.garden.fields)

        for index, field in enumerate(self.garden.fields):
            print(f"Field {index + 1}: {field.assigned_crop.name.capitalize().ljust(9) if field.assigned_crop else 'EMPTY'.ljust(9)}: €{field.seasonal_harvest}")
        press_enter()