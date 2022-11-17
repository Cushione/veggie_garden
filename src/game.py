from random import choice
from string import ascii_uppercase
from .utils import SHEET, valid_string_input, press_enter, new_page, Colors, colored_string, Text
from .player import Player

class Game:
    def __init__(self, new_game):
        self.games_sheet = SHEET.worksheet("games")
        if new_game:
            self.new_game()
        else:
            self.load_game()
        self.play_game()

    def new_game(self):
        new_page(None, *Text.USERNAME)
        self.username = valid_string_input("Please enter your username: ", 3, 20)
        self.id = "".join(choice(ascii_uppercase) for i in range(6))
        new_page(None, *Text.game_id(self.id))
        press_enter()
        new_page(None)
        print(colored_string(Colors.yellow, "Loading..."))
        self.player = Player(self, 20)
        self.save_game(False)

    def load_game(self):
        prev_id = input("Please enter your id: ")
        prev_game_row = self.games_sheet.find(prev_id).row
        prev_game = self.games_sheet.row_values(prev_game_row)
        self.id = prev_game[0]
        self.username = prev_game[1]

    def save_game(self, update=True):
        game_data = [self.id, self.username, *self.player.get_progress()]
        if update:
            prev_game = self.games_sheet.find(self.id)
            row = prev_game.row
            self.games_sheet.update(f"c{row}:o{row}", [game_data[2:]])
        else:
            self.games_sheet.append_row(game_data)

    def play_game(self):
        if self.player.prepare_next_season():
            self.show_game_results()

    def show_game_results(self):
        new_page(None, *Text.end_screen(self))
        press_enter()
