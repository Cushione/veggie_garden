from .utils import SHEET, valid_number_input, valid_confirm_input, press_enter


class Fertiliser():

    def __init__(self, level):
        self.level = level
        self.load_fertiliser_data()

    def load_fertiliser_data(self):
        fertiliser_sheet = SHEET.worksheet("fertiliser")
        self.prices = [int(price) for price in fertiliser_sheet.col_values(2)[1:]]
        self.rewards = [float(reward) for reward in fertiliser_sheet.col_values(3)[1:]]

    def upgrade(self):
        self.level += 1

    def improve_harvest(self, harvest):
        return round(harvest * self.rewards[self.level])

    def display_fertiliser_menu(self, player):
        while True:
            print("Fertiliser")
            for index, name in enumerate(["Basic Fertiliser", "Advanced Fertiliser", "Super Fertiliser"]):
                print(f"{name.ljust(20)}: {'UNLOCKED' if self.level == index + 1 else f'€{self.prices[index + 1]}'}")

            print("1: Upgrade Fertiliser")
            print("0: Go Back")
            user_input = valid_number_input("What would you like to do?: ", 0, 1)
            if user_input == 1:
                price = self.prices[self.level + 1]
                if valid_confirm_input(f"Are you sure you want to upgrade your Fertiliser for €{price}?: "):
                    if player.money >= price:
                        player.money -= price
                        self.upgrade()
                    else:
                        print("Insufficient funds!")
                        press_enter()
            else:
                break

