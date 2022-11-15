from .utils import CROPS

class Storage():
    def __init__(self, seeds):
        self.seeds = self.init_seeds(seeds)

    def init_seeds(self, seeds):
        return dict(zip([crop.name for crop in CROPS], seeds))

    def available_seeds(self, crop):
        return self.seeds[crop]