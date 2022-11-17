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

    def not_ripe(self, month):
        print(f"{self.name.capitalize()} is not ripe yet.")


class Tree(Crop):
    def __init__(self, name, reward, harvest_time, planted=None):
        super().__init__(name, reward, harvest_time)
        self.planted = planted
        self.perennial = True

    def is_ripe(self, month):
        return month % 6 == 0 and (month - self.planted) >= self.harvest_time

    def plant(self, month):
        self.planted = month

    def not_ripe(self, month):
        if month % 6 != 0:
            print(f"{self.name.capitalize()} is not ripe yet.")
        else:
            print(f"{self.name.capitalize()} grew a little.")