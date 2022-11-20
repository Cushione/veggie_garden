"""
Storage Module.
"""
from .utils import SHEET, press_enter
from .crop import Tree, Crop


class Storage:
    """
    Representation of the storage object.
    Loads crop data from Google sheets upon initialisation.
    Keeps track of seeds and returns crop object for planting.
    """
    def __init__(self, amounts):
        self.load_seeds(amounts)

    def load_seeds(self, amounts):
        """
        Loads crop data from Google sheets.
        """
        crop_sheet = SHEET.worksheet("crops")
        # Create dictionaries with crops names as keys
        self.names = crop_sheet.col_values(1)[1:]
        # Map crop names to crop amounts
        self.seeds = dict(zip(self.names, amounts))
        # Map crop names to crop data
        self.crops = dict(zip(self.names, crop_sheet.get_all_values()[1:]))

    def available_seeds(self, crop):
        """
        Returns amount of available seeds of a specific crop.
        """
        return self.seeds[crop]

    def add_seeds(self, crop, amount):
        """
        Adds specified amount of seeds to the storage.
        """
        self.seeds[crop] += amount

    def take_seed(self, name):
        """
        Takes a seed of the specified crop from the storage.
        Returns an instance of the crop.
        """
        self.seeds[name] -= 1
        return self.create_crop(self.names.index(name))

    def create_crop(self, value):
        """
        Creates an instance of the specified crop.
        """
        # If value is greater than 3, then create a Tree
        if value > 3:
            # Tree can only be planted between seasons when the month is
            # a multiple of 6
            planted = int(value / 6) * 6
            # The rest equals the index of the crop
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
        """
        Displays a numbered list of all crops with their respective amount
        of seeds.
        """
        for index, crop in enumerate(self.seeds):
            print(
                f"{index + 1}: {crop.capitalize().ljust(9)}: "
                + f"{self.seeds[crop]}"
            )

    def display_storage_menu(self):
        """
        Displays storage menu, a list of all crops with their respective
        amount of seeds.
        """
        for crop, amount in self.seeds.items():
            print(f"{crop.capitalize().ljust(9)}: {amount}")
        press_enter("Press Enter to go back. ")
