from .utils import CROPS

class Storage():
    def __init__(self, seeds):
        self.seeds = self.init_seeds(seeds)

    def init_seeds(self, seeds):
        return dict(zip([crop for crop in CROPS], seeds))

    def available_seeds(self, crop):
        return self.seeds[crop]

    def add_seeds(self, crop, amount):
        self.seeds[crop] = self.seeds[crop] + amount

    def display_available_seeds(self):
        for index, crop in enumerate(self.seeds):
            print(f"{index + 1}:  {crop}: {self.seeds[crop]}")

    def display_storage_menu(self):
        for crop, amount in self.seeds.items():
            print(f"{crop}: {amount}")
        
        input("Press Enter to go back. ")
        