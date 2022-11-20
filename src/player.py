"""
Player Module.
"""
from .events import Events
from .storage import Storage
from .fertiliser import Fertiliser
from .field import Field
from .garden import Garden
from .store import Store
from .utils import (
    valid_number_input,
    press_enter,
    MONTHS,
    new_page,
    colored_string,
    Colors,
    valid_confirm_input,
    Text,
)
import time


class Player:
    """
    Representation of the Player object.
    Binds together all the game elements and handles the main game logic.
    """
    def __init__(
        self,
        game,
        money=20,
        month=0,
        seeds=[0, 0, 0, 0, 0],
        fertiliser=0,
        fields=[-1],
    ):
        self.money = money
        self.month = month
        self.events = Events()
        self.storage = Storage(seeds)
        self.fertiliser = Fertiliser(fertiliser)
        self.garden = Garden(fields, self.storage, self.fertiliser)
        self.store = Store()
        self.game = game

    def prepare_next_season(self):
        """
        Allows the user to prepare for the next season.
        Displays the main game menu from where the user can access all the
        game elements.
        The loop finishes when the game reaches month 60.
        """
        while True:
            new_page(self.game, *Text.prepare_season(self.month))
            print("1: Open Storage")
            print("2: Fertiliser")
            print("3: Visit Store")
            print("4: Go to Fields")
            print("5: Start season")
            print("0: Save and Exit")
            user_input = valid_number_input(
                "What would you like to do next?: ", 0, 5
            )

            if user_input == 1:
                new_page(self.game, *Text.STORAGE)
                self.storage.display_storage_menu()
            elif user_input == 2:
                self.fertiliser.display_fertiliser_menu(self)
            elif user_input == 3:
                self.store.buy_seeds(self)
            elif user_input == 4:
                self.garden.display_field_menu(self)
            elif user_input == 5:
                new_page(self.game, *Text.NEXT_SEASON)
                if valid_confirm_input(
                    "Are you sure you want to start the next season?: "
                ):
                    self.work_season()
            else:
                new_page(self.game, *Text.SAVE_EXIT)
                if valid_confirm_input(
                    "Are you sure you want to leave the game?: "
                ):
                    return False
            self.game.save_game()

            if self.month == 60:
                return True

    def work_season(self):
        """
        Works a season by tending to all unlocked fields 6 times.
        """
        new_page(self.game)
        year = int(self.month / 6) + 1
        print(
            colored_string(
                Colors.green,
                f"\n----- {f'Start of Year {year}'.center(17)} -----",
            )
        )
        for month in range(6):
            month_name = colored_string(
                Colors.rgb(255, 100, 255), MONTHS[month].center(17)
            )
            print(f"\n----- {month_name} -----")
            time.sleep(0.5)
            self.month += 1
            if not any([field.is_filled() for field in self.garden.fields]):
                print("\nAll fields are empty.")
                time.sleep(1)
                continue
            for index, field in enumerate(self.garden.fields):
                if not field.is_filled():
                    continue
                print(
                    f"\n--- {f'Tending to field {index + 1}'.center(21)} ---"
                )
                time.sleep(0.5)
                field.tend(self.month)
                time.sleep(1)
        print(
            colored_string(
                Colors.green,
                f"\n----- {f'End of Year {year}'.center(17)} -----",
            )
        )
        press_enter("Press Enter to see your profits.")
        self.handle_end_of_season()

    def handle_end_of_season(self):
        """
        Handles the end of a season.
        Determines if an event happend and adjusts harvest accordingly.
        Afterwards, shows the overview, adds profit to the money and
        plows (resets) all the fields.
        """
        event = self.events.get_random_event()
        if event is not None:
            event.adjust_harvest(self.garden.fields)
        self.season_overview(event)

        for field in self.garden.fields:
            self.money += field.seasonal_harvest
            field.plow()

    def season_overview(self, event):
        """
        Displays an overview of the recent season.
        Shows a description of the event if applicable and an overview of 
        the profits.
        """
        new_page(self.game, Text.SEASON_OVERVIEW)
        if event is not None:
            event.print_self()
        total_profit = 0
        for index, field in enumerate(self.garden.fields):
            status = (
                field.assigned_crop.name.capitalize().ljust(9)
                if field.assigned_crop
                else "EMPTY".ljust(9)
            )
            print(
                f"Field {index + 1}: {status}: "
                + f"{f'€{field.seasonal_harvest}'.rjust(7)}"
            )
            total_profit += field.seasonal_harvest
        print("---------------------------")

        print(f"Total Profit:{f'€{total_profit}'.rjust(14)}")
        press_enter()

    def get_progress(self):
        """
        Collects data from all game elements and returns them as a list.
        """
        return [
            self.money,
            self.month,
            self.fertiliser.level,
            *self.storage.seeds.values(),
            *self.garden.get_field_status(),
        ]
