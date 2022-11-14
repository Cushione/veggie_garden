from random import choice
from string import ascii_uppercase

class Game():
    def __init__(self, username, games_sheet):
        self.username = username
        self.games_sheet = games_sheet
        self.save_game()

    def save_game(self, update=True):
        if update:
            prev_game = self.games_sheet.find("RZOFYK")
            row = prev_game.row
            self.games_sheet.update(f"c{row}:d{row}", [["1", "1"]])
        else:
            self.id = "".join(choice(ascii_uppercase) for i in range(6))
            self.games_sheet.append_row([self.id, self.username, 0, 0])



