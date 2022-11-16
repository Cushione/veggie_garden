from .utils import SHEET, CROPS, valid_number_input
from .crop import Crop, Tree


class Field():

    def __init__(self, crop, seasonal_harvest, storage):
        try:
            crop
        except NameError:
            self.crop = None
        else:
            self.crop = crop
        self.seasonal_harvest = seasonal_harvest
        self.storage = storage

    def tend(self, month):
        if self.is_filled() and self.crop.is_ripe(month):
            self.seasonal_harvest += self.crop.harvest()
            if self.storage.available_seeds(self.crop.name) > 0:
                self.storage.take_seeds(self.crop.name)
            else:
                self.crop = None

    def is_filled(self):
        return self.crop is not None

class Fields():

    def __init__(self, fields_data, storage):
        self.fields = [Field(crop, seasonal_harvest, storage) for crop, seasonal_harvest in fields_data]
        self.load_prices()
        self.storage = storage

    def load_prices(self):
        price_sheet = SHEET.worksheet("fields")
        self.prices = [int(price) for price in price_sheet.col_values(1)[1:]]

    def display_field_menu(self, player):
        while True:
            print("Fields")
            for index in range(0, 5):
                print(f"Field {index + 1}:  {(self.fields[index].crop if self.fields[index].crop.name else 'READY TO PLANT') if len(self.fields) >= index + 1 else f'€{self.prices[index]}'}")

            print("1: Unlock new field")
            print("2: Plant crops")
            print("0: Go Back")
            user_input = valid_number_input("What would you like to do?: ", 0, 2)
            if user_input == 1:
                self.unlock_new_field(player)
            elif user_input == 2:
                self.assign_crops(player)
            else:
                break

    def unlock_new_field(self, player):
        # TODO: Confirm unlock
        if player.money >= self.prices[len(self.fields)]:
            player.money -= self.prices[len(self.fields)]
            self.fields.append(Field(None, 0, self.storage))
        else:
            print("Insufficient funds!")
            input("Press Enter to continue.")

    def assign_crops(self, player):
        while True:
            for index, field in enumerate(self.fields):
                print(f"{index + 1}: Field {index + 1} - {field.crop.name if field.is_filled() else 'EMPTY'}")
            print("0: Go Back")
            selected_field = valid_number_input("Select a field: ", 0, len(self.fields))
            if selected_field == 0:
                break
            while True:
                self.storage.display_available_seeds()
                print("0: Go Back")
                selected_crop = valid_number_input("What crop would you like to plant?: ", 0, 5)
                if selected_crop == 0:
                    break
                if self.storage.available_seeds(CROPS[selected_crop-1]) == 0:
                    print("Not enough seeds. Go to Store to buy more.")
                    input("Press Enter to continue.")
                else:
                    crop = self.storage.take_seed(selected_crop - 1)
                    crop.plant(player.month)
                    self.fields[selected_field-1].crop = crop
                    break
