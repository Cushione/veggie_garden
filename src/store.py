from .utils import SHEET, CROPS, valid_number_input


class Store:
    def __init__(self):
        self.prices = self.load_prices()

    def load_prices(self):
        prices_sheet = SHEET.worksheet("crops")
        return [int(price) for price in prices_sheet.col_values(2)[1:]]

    def buy_seeds(self, player):
        success = False
        while not success:
            self.show_stock()
            selected_index = self.select_crop() - 1

            if player.money < self.prices[selected_index]:
                print("You cannot afford this packet of seeds!")
                continue
            amount, total_price = self.select_amount(
                selected_index, player.money
            )

            confirm = input(
                f"Are you sure you want to buy {amount} packets of {CROPS[selected_index]} for €{total_price}?: "
            )
            if confirm == "y":
                player.money -= total_price
                player.storage.add_seeds(CROPS[selected_index], amount)
                success = True
            else:
                continue

    def show_stock(self):
        for index, crop in enumerate(CROPS):
            print(f"{index + 1}. {crop} - €{self.prices[index]}")

    def select_crop(self):
        return valid_number_input("What would you like to buy? (1-5): ", 1, 5)

    def select_amount(self, selected_index, budget):
        valid_amount = False
        while not valid_amount:
            amount = valid_number_input("How many packets would you like to buy?: ", 1, 99)
            total_price = self.prices[selected_index] * amount
            if budget >= total_price:
                valid_amount = True
            else:
                print("Insufficient funds!")
        return (amount, total_price)
