
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