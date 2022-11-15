from .utils import SHEET

class Storage():
    def __init__(self, seeds):
        self.seeds = self.init_seeds(seeds)

    def init_seeds(self, seeds):
        crops_sheet = SHEET.worksheet("crops")
        crops_data = crops_sheet.col_values(1)
        return dict(zip(crops_data[1:], seeds))

    def available_seeds(self, crop):
        return self.seeds[crop]