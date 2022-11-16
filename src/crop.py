class Crop():
    def __init__(self, name, reward, harvest_time):
        self.name = name
        self.reward = reward
        self.harvest_time = harvest_time
        self.perennial = False

    def is_ripe(self, month):
        return month % self.harvest_time == 0

    def plant(self, month):
        pass

    def harvest(self, month):
        return self.reward if self.is_ripe(month) else 0


class Tree(Crop):
    def __init__(self, name, reward, harvest_time):
        super().__init__(name, reward, harvest_time)
        self.planted = None
        self.perennial = True

    def is_ripe(self, month):
        return month % 6 == 0 and (month - self.planted) >= self.harvest_time

    def plant(self, month):
        self.planted = month