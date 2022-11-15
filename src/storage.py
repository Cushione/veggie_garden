from .utils import SHEET
from .crop import Tree, Crop

class Storage():
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

    def take_seed(self, index):
        name = self.names[index]
        self.seeds[name] -= 1
        crop = self.crops[name]
        if name == self.names[-1]:
            return Tree(crop[0], crop[2], crop[3])
        else:
            return Crop(crop[0], crop[2], crop[3])

    def display_available_seeds(self):
        for index, crop in enumerate(self.seeds):
            print(f"{index + 1}:  {crop}: {self.seeds[crop]}")

    def display_storage_menu(self):
        for crop, amount in self.seeds.items():
            print(f"{crop}: {amount}")
        
        input("Press Enter to go back. ")
        