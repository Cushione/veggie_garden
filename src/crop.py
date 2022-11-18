"""
Crop and Tree Module.
"""


class Crop:
    """
    Representation of a crop object.
    Handles the ripening of crop and returns its reward upon harvest.
    """
    def __init__(self, name, reward, harvest_time):
        self.name = name
        self.reward = reward
        self.harvest_time = harvest_time
        self.perennial = False
        self.planted = 0

    def is_ripe(self, month):
        """
        Returns true or false for whether the crop is ready for harvest.
        """
        return month % self.harvest_time == 0

    def plant(self, month):
        """
        Plants the crop.
        Stores the month of planting.
        """
        self.planted = month

    def harvest(self, month):
        """
        Harvests the crop.
        Returns profit from the harvest.
        """
        return self.reward if self.is_ripe(month) else 0

    def not_ripe(self, month):
        """
        Prints information about the crop not being ready for harvest.
        """
        print(f"{self.name.capitalize()} is not ripe yet.")


class Tree(Crop):
    """
    Representation of a tree object.
    Handles the ripening of tree and returns its reward upon harvest.
    """
    def __init__(self, name, reward, harvest_time, planted=None):
        super().__init__(name, reward, harvest_time)
        self.planted = planted
        self.perennial = True

    def is_ripe(self, month):
        return month % 6 == 0 and (month - self.planted) >= self.harvest_time

    def not_ripe(self, month):
        if (month - self.planted) <= self.harvest_time - 6:
            print(f"{self.name.capitalize()} grew a little.")
        else:
            super().not_ripe(month)
