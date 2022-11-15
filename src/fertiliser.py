from .utils import SHEET


class Fertiliser():

    def __init__(self, level):
        self.level = level
        self.rewards = self.load_rewards()

    def load_rewards(self):
        fertiliser_sheet = SHEET.worksheet("fertiliser")
        return fertiliser_sheet.col_values(3)[1:]


    def upgrade(self):
        self.level += 1
