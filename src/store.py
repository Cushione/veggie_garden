"""
Store Module.
"""
from .utils import (
    SHEET,
    CROPS,
    valid_number_input,
    valid_confirm_input,
    press_enter,
    new_page,
    Text,
    print_error,
)


class Store:
    """
    Representation of the store object.
    Allows the user to buy new seeds for planting.
    Loads prices from Google sheets.
    """
    def __init__(self):
        self.prices = self.load_prices()

    def load_prices(self):
        """
        Loads prices from Google sheets and returns them as a list.
        """
        prices_sheet = SHEET.worksheet("crops")
        return [int(price) for price in prices_sheet.col_values(2)[1:]]

    def buy_seeds(self, player):
        """
        Allows the user to buy new seeds for planting.
        Displays the stock and allows the user to select a crop and amount.
        After confirming, the seeds are added to the storage.
        """
        while True:
            new_page(player.game, *Text.STORE)
            self.show_stock()
            print("0: Go back")
            selected_index = self.select_crop()

            if selected_index == 0:
                break
            selected_crop = selected_index - 1

            if player.money < self.prices[selected_crop]:
                print_error("You cannot afford this packet of seeds!")
                press_enter()
                continue
            amount, total_price = self.select_amount(
                selected_crop, player.money
            )

            new_page(player.game)
            if valid_confirm_input(
                f"Are you sure you want to buy {amount} packets of "
                + f"{CROPS[selected_crop]} for €{total_price}?: "
            ):
                player.money -= total_price
                player.storage.add_seeds(CROPS[selected_crop], amount)

    def show_stock(self):
        """
        Displays store stock and prices as a numbered list.
        """
        for index, crop in enumerate(CROPS):
            print(
                f"{index + 1}: {crop.capitalize().ljust(9)}: "
                + f"€{self.prices[index]}"
            )

    def select_crop(self):
        """
        Handles the user input for the crop selection.
        """
        while True:
            selected = valid_number_input(
                "What would you like to buy?: ", 0, 5
            )
            if selected == 5:
                print(
                    "Avocado is a perenial. It takes a few seasons "
                    + "to be ready to harvest."
                )
                if not valid_confirm_input(
                    "Do you still want to buy this seed?: "
                ):
                    continue
            break
        return selected

    def select_amount(self, selected_index, budget):
        """
        Handles the user input for the amount of seeds they want to buy.
        """
        while True:
            amount = valid_number_input(
                "\nHow many packets would you like to buy?: ", 1, 99
            )
            total_price = self.prices[selected_index] * amount
            if budget >= total_price:
                break
            else:
                print_error("Insufficient funds!")
                press_enter()
        return (amount, total_price)
