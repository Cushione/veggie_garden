from .utils import SHEET
from random import shuffle, random

class Events():
    def __init__(self):
        self.load_events()

    def load_events(self):
        events_sheet = SHEET.worksheet("special_events")
        events_data = events_sheet.get_all_values()
        self.events = [Event(x) for x in events_data[1:]]

    def get_random_event(self):
        shuffle(self.events)
        for event in self.events:
            if random() <= event.chance:
                return event
        return None

class Event():
    def __init__(self, data):
        self.name = data[0]
        self.chance = float(data[1])
        self.effect = float(data[2])
        self.description = data[3]

    def adjust_harvest(self, fields):
        for field in fields:
            field.seasonal_harvest = round(field.seasonal_harvest * self.effect)