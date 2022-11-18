from .field import Field
from .utils import (
    SHEET,
    new_page,
    Text,
    print_error,
    valid_number_input,
    valid_confirm_input,
    press_enter,
    CROPS,
)


class Garden:
    def __init__(self, fields_data, storage, fertiliser):
        self.fields = [
            Field(status, storage, fertiliser)
            for status in fields_data
            if status >= -1
        ]
        self.load_prices()
        self.storage = storage

    def load_prices(self):
        price_sheet = SHEET.worksheet("fields")
        self.prices = [int(price) for price in price_sheet.col_values(1)[1:]]

    def display_field_menu(self, player):
        while True:
            new_page(player.game, *Text.FIELDS)
            for index in range(0, 5):
                status = (
                    (
                        self.fields[index].crop.name.capitalize()
                        if self.fields[index].crop
                        else "READY TO PLANT"
                    )
                    if len(self.fields) >= index + 1
                    else f"€{self.prices[index]}"
                )
                print(f"Field {index + 1} : {status}")
            print("\n1: Plant crops")
            if len(self.fields) < 5:
                print("2: Unlock new field")
            print("0: Go Back")
            user_input = valid_number_input(
                "What would you like to do?: ",
                0,
                2 if len(self.fields) < 5 else 1,
            )
            if user_input == 1:
                self.assign_crops(player)
            elif user_input == 2 and len(self.fields) < 5:
                self.unlock_new_field(player)
            else:
                break

    def unlock_new_field(self, player):
        new_page(player.game, *Text.UNLOCK_NEW_FIELD)
        price = self.prices[len(self.fields)]
        if valid_confirm_input(
            f"Are you sure you want to unlock the next field for €{price}?: "
        ):
            if player.money >= price:
                player.money -= price
                self.fields.append(Field(-1, self.storage, player.fertiliser))
            else:
                print_error("Insufficient funds!")
                press_enter()

    def assign_crops(self, player):
        while True:
            new_page(player.game, *Text.ASSIGN_CROPS)
            for index, field in enumerate(self.fields):
                status = (
                    field.crop.name.capitalize()
                    if field.is_filled()
                    else "EMPTY"
                )
                print(f"{index + 1}: Field {index + 1} : {status}")
            print("0: Go Back")
            selected_field = valid_number_input(
                "Select a field: ", 0, len(self.fields)
            )
            if selected_field == 0:
                break
            elif self.fields[
                selected_field - 1
            ].is_filled() and not valid_confirm_input(
                "Are you sure you want to plant a new crop in this field? "
                + "Your current crop will be lost.: "
            ):
                continue
            while True:
                new_page(player.game, Text.AVAILABLE_SEEDS)
                self.storage.display_available_seeds()
                print("0: Go Back")
                selected_crop = valid_number_input(
                    "What crop would you like to plant?: ", 0, 5
                )
                if selected_crop == 0:
                    break
                if self.storage.available_seeds(CROPS[selected_crop - 1]) == 0:
                    print_error("Not enough seeds. Go to Store to buy more.")
                    press_enter()
                else:
                    crop = self.storage.take_seed(CROPS[selected_crop - 1])
                    crop.plant(player.month)
                    self.fields[selected_field - 1].assign_crop(crop)
                    break

    def get_field_status(self):
        fields = [-2 for i in range(5)]
        for index, field in enumerate(self.fields):
            crop = CROPS.index(field.crop.name) if field.crop else -1
            if crop == 4:
                crop += field.crop.planted
            fields[index] = crop
        return fields
