from .utils import SHEET

class Events():
    def __init__(self):
        self.events = self.load_events()

    def load_events(self):
        events_sheet = SHEET.worksheet("special_events")
        events_data = events_sheet.get_all_values()
        events_list = [Event(x) for x in events_data[1:]]
        return {event.name: event for event in events_list}

class Event():
    def __init__(self, data):
        self.name = data[0]
        self.chance = data[1]
        self.effect = data[2]
        self.description = data[3]