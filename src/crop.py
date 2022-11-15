class Crop():
    def __init__(self, name, reward, harvest_time):
        self.name = name
        self.reward = reward
        self.harvest_time = harvest_time

    def is_ripe(self, month):
        return month % self.harvest_time == 0


class Tree(Crop):
    def __init__(self, name, reward, harvest_time, planted, storage):
        super().__init__(name, reward, harvest_time, storage)
        self.planted = planted

    def is_ripe(self, month):
        return month % 6 == 0 and (self.planted - month) <= self.harvest_time