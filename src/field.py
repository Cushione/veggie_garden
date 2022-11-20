"""
Field Module.
"""
import time


class Field:
    """
    Representation of a field object.
    Stores assigned crop and seasonal harvest.
    Handles harvesting and replanting of its crop.
    """
    def __init__(self, status, storage, fertiliser):
        self.seasonal_harvest = 0
        self.storage = storage
        self.fertiliser = fertiliser
        # Field is empty
        if status == -1:
            self.crop = None
            self.assigned_crop = None
        # Field has a crop
        else:
            crop = self.storage.create_crop(status)
            self.crop = crop
            self.assigned_crop = crop

    def tend(self, month):
        """
        Called every month of the growing season.
        Checks if assigned crop is ripe, and if applicable, applies
        fertiliser, harvests and replants the crop.
        """
        if self.is_filled() and self.crop.is_ripe(month):
            print(f"Harvesting {self.crop.name}.")
            time.sleep(0.5)
            self.seasonal_harvest += self.fertiliser.improve_harvest(
                self.crop.harvest(month)
            )
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
        """
        Returns true or false for whether a crop is assigned to the field.
        """
        return self.crop is not None

    def assign_crop(self, crop):
        """
        Assigns a crop to the field.
        """
        self.crop = crop
        self.assigned_crop = crop

    def plow(self):
        """
        Plows the field at the end of a season.
        Resets the seasonal harvest and assigned crop.
        """
        self.seasonal_harvest = 0
        if self.assigned_crop and not self.assigned_crop.perennial:
            self.assigned_crop = None
