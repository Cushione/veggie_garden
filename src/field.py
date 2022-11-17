from .utils import SHEET, CROPS, valid_number_input, valid_confirm_input, press_enter, new_page, Text, print_error
from .crop import Crop, Tree
import time

class Field():

    def __init__(self, crop, seasonal_harvest, storage, fertiliser):
        try:
            crop
        except NameError:
            self.crop = None
            self.assigned_crop = None
        else:
            self.crop = crop
            self.assigned_crop = crop
        self.seasonal_harvest = seasonal_harvest
        self.storage = storage
        self.fertiliser = fertiliser

    def tend(self, month):
        if self.is_filled() and self.crop.is_ripe(month):
            print(f"Harvesting {self.crop.name}.")
            time.sleep(0.5)
            self.seasonal_harvest += self.fertiliser.improve_harvest(self.crop.harvest(month)) 
            if not self.crop.perennial:
                if month % 6 != 0:
                    if self.storage.available_seeds(self.crop.name) > 0:
                        print(f"Replanting {self.crop.name}.")
                        self.storage.take_seed(self.crop.name)
                    else:
                        print(f"No more {self.crop.name} seeds to plant.")  
                        self.crop = None
                else:
                    self.crop = None
        elif self.is_filled():
            self.crop.not_ripe(month)

    def is_filled(self):
        return self.crop is not None

    def assign_crop(self, crop):
        self.crop = crop
        self.assigned_crop = crop

    def plow(self):
        self.seasonal_harvest = 0
        if self.assigned_crop and not self.assigned_crop.perennial:
            self.assigned_crop = None

class Garden():

    def __init__(self, fields_data, storage, fertiliser):
        self.fields = [Field(crop, seasonal_harvest, storage, fertiliser) for crop, seasonal_harvest in fields_data]
        self.load_prices()
        self.storage = storage

    def load_prices(self):
        price_sheet = SHEET.worksheet("fields")
        self.prices = [int(price) for price in price_sheet.col_values(1)[1:]]

    def display_field_menu(self, player):
        while True:
            new_page(player.game, *Text.FIELDS)
            for index in range(0, 5):
                print(f"Field {index + 1} : {(self.fields[index].crop.name.capitalize() if self.fields[index].crop else 'READY TO PLANT') if len(self.fields) >= index + 1 else f'€{self.prices[index]}'}")

            print("\n1: Plant crops")
            print("2: Unlock new field")
            print("0: Go Back")
            user_input = valid_number_input("What would you like to do?: ", 0, 2)
            if user_input == 1:
                self.assign_crops(player)
            elif user_input == 2:
                self.unlock_new_field(player)
            else:
                break

    def unlock_new_field(self, player):
        new_page(player.game, *Text.UNLOCK_NEW_FIELD)
        price = self.prices[len(self.fields)]
        if valid_confirm_input(f"Are you sure you want to unlock the next field for €{price}?: "):
            if player.money >= price:
                player.money -= price
                self.fields.append(Field(None, 0, self.storage, player.fertiliser))
            else:
                print_error("Insufficient funds!")
                press_enter()

    def assign_crops(self, player):
        while True:
            new_page(player.game, *Text.ASSIGN_CROPS)
            for index, field in enumerate(self.fields):
                print(f"{index + 1}: Field {index + 1} : {field.crop.name.capitalize() if field.is_filled() else 'EMPTY'}")
            print("0: Go Back")
            selected_field = valid_number_input("Select a field: ", 0, len(self.fields))
            if selected_field == 0:
                break
            elif self.fields[selected_field-1].is_filled() and not valid_confirm_input("Are you sure you want to plant a new crop in this field? Your current crop will be lost.: "):
                continue
            while True:
                new_page(player.game, Text.AVAILABLE_SEEDS)
                self.storage.display_available_seeds()
                print("0: Go Back")
                selected_crop = valid_number_input("What crop would you like to plant?: ", 0, 5)
                if selected_crop == 0:
                    break
                if self.storage.available_seeds(CROPS[selected_crop-1]) == 0:
                    print_error("Not enough seeds. Go to Store to buy more.")
                    press_enter()
                else:
                    crop = self.storage.take_seed(CROPS[selected_crop - 1])
                    crop.plant(player.month)
                    self.fields[selected_field-1].assign_crop(crop)
                    break
