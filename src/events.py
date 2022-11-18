"""
Event Module.
"""
from .utils import SHEET
from random import shuffle, random


class Events:
    """
    Class for handling events.
    Loads event data from Google sheets on initialisation and creates
    a list of events.
    """
    def __init__(self):
        self.load_events()

    def load_events(self):
        """
        Loads event data from Google sheets and stores it as a list of
        event objects.
        """
        events_sheet = SHEET.worksheet("special_events")
        events_data = events_sheet.get_all_values()
        self.events = [Event(x) for x in events_data[1:]]

    def get_random_event(self):
        """
        Returns a random event or None.
        """
        shuffle(self.events)
        for event in self.events:
            if random() <= event.chance:
                return event
        return None


class Event:
    """
    Representation of an event.
    Holds all the event data and can adjust harvest.
    """
    def __init__(self, data):
        self.name = data[0]
        self.chance = float(data[1])
        self.effect = float(data[2])
        self.description = data[3]

    def adjust_harvest(self, fields):
        """
        Adjust a seasonal harvest with the respective event effect.
        """
        for field in fields:
            field.seasonal_harvest = round(
                field.seasonal_harvest * self.effect
            )

    def print_self(self):
        """
        Prints the event description.
        """
        print(f"{self.description}\n")
