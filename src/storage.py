from .utils import SHEET, press_enter
from .crop import Tree, Crop


class Storage:
    def __init__(self, amounts):
        self.load_seeds(amounts)

    def load_seeds(self, amounts):
        crop_sheet = SHEET.worksheet("crops")
        self.names = crop_sheet.col_values(1)[1:]
        self.seeds = dict(zip(self.names, amounts))
        self.crops = dict(zip(self.names, crop_sheet.get_all_values()[1:]))

    def available_seeds(self, crop):
        return self.seeds[crop]

    def add_seeds(self, crop, amount):
        self.seeds[crop] += amount

    def take_seed(self, name):
        self.seeds[name] -= 1
        return self.create_crop(self.names.index(name))

    def create_crop(self, value):
        if value > 3:
            planted = int(value / 6) * 6
            index = value % 6
            name = self.names[index]
            return Tree(
                name,
                int(self.crops[name][2]),
                int(self.crops[name][3]),
                planted,
            )
        name = self.names[value]
        return Crop(name, int(self.crops[name][2]), int(self.crops[name][3]))

    def display_available_seeds(self):
        for index, crop in enumerate(self.seeds):
            print(
                f"{index + 1}: {crop.capitalize().ljust(9)}: "
                + f"{self.seeds[crop]}"
            )

    def display_storage_menu(self):
        for crop, amount in self.seeds.items():
            print(f"{crop.capitalize().ljust(9)}: {amount}")
        press_enter("Press Enter to go back. ")
