"""
Fertiliser Module.
"""
from .utils import (
    SHEET,
    valid_number_input,
    valid_confirm_input,
    press_enter,
    new_page,
    Text,
    print_error
)


class Fertiliser:
    """
    Representation of the fertiliser object.
    Loads fertiliser data from Google sheets upon initialisation.
    Manages the current fertiliser level.
    """
    def __init__(self, level):
        self.level = level
        self.load_fertiliser_data()

    def load_fertiliser_data(self):
        """
        Loads fertiliser data from Google sheets.
        """
        fertiliser_sheet = SHEET.worksheet("fertiliser")
        # Extract prices and rewards from the data
        self.prices = [
            int(price) for price in fertiliser_sheet.col_values(2)[1:]
        ]
        self.rewards = [
            float(reward) for reward in fertiliser_sheet.col_values(3)[1:]
        ]

    def upgrade(self):
        """
        Increments the fertiliser level.
        """
        self.level += 1

    def improve_harvest(self, harvest):
        """
        Adjusts seasonal harvest with the respective reward.
        """
        return round(harvest * self.rewards[self.level])

    def display_fertiliser_menu(self, player):
        """
        Displays the fertiliser menu.
        Allows the user to see the current level of fertiliser and upgrade
        if the user has enough money.
        """
        while True:
            new_page(player.game, *Text.FERTILISER)
            for index, name in enumerate(
                ["Basic Fertiliser", "Advanced Fertiliser", "Super Fertiliser"]
            ):
                status = (
                    "UNLOCKED"
                    if self.level >= index + 1
                    else f"€{self.prices[index + 1]}"
                )
                print(f"{name.ljust(20)}: {status}")
            if self.level < 3:
                print("\n1: Upgrade Fertiliser")
                print("0: Go Back")
                user_input = valid_number_input(
                    "What would you like to do?: ", 0, 1
                )
                if user_input == 1:
                    new_page(player.game, Text.UPGRADE_FERTILISER)
                    price = self.prices[self.level + 1]
                    if valid_confirm_input(
                        "Are you sure you want to upgrade your fertiliser "
                        + f"for €{price}?: "
                    ):
                        if player.money >= price:
                            player.money -= price
                            self.upgrade()
                        else:
                            print_error("Insufficient funds!")
                            press_enter()
                else:
                    break
            else:
                press_enter("Press Enter to go back.")
                break
