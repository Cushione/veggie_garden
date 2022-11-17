from .crop import Crop, Tree
import time

class Field():

    def __init__(self, crop, storage, fertiliser):
        try:
            crop
        except NameError:
            self.crop = None
            self.assigned_crop = None
        else:
            self.crop = crop
            self.assigned_crop = crop
        self.seasonal_harvest = 0
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
