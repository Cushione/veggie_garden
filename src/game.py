from random import choice
from string import ascii_uppercase
from utils import SHEET


class Game:
    def __init__(self, new_game):
        self.games_sheet = SHEET.worksheet("games")
        if new_game:
            self.new_game()
        else:
            self.load_game()

    def new_game(self):
        self.username = input("Please enter your username: ")
        self.id = "".join(choice(ascii_uppercase) for i in range(6))
        self.save_game(False)

    def load_game(self):
        prev_id = input("Please enter your id: ")
        prev_game_row = self.games_sheet.find(prev_id).row
        prev_game = self.games_sheet.row_values(prev_game_row)
        self.id = prev_game[0]
        self.username = prev_game[1]

    def save_game(self, update=True):
        if update:
            prev_game = self.games_sheet.find(self.id)
            row = prev_game.row
            self.games_sheet.update(f"c{row}:d{row}", [["1", "1"]])
        else:
            self.games_sheet.append_row([self.id, self.username, 0, 0])
