"""
Game Module.
"""
from random import choice
from string import ascii_uppercase
from .utils import (
    SHEET,
    valid_string_input,
    press_enter,
    new_page,
    Colors,
    colored_string,
    Text,
    print_error,
    valid_confirm_input,
)
from .player import Player


class Game:
    """
    Representation of a game object.
    Handles the start of a new game and saving and loading of existing games.
    """
    def __init__(self, new_game):
        self.games_sheet = SHEET.worksheet("games")
        self.id = None
        self.username = None
        self.player = None
        if new_game:
            self.new_game()
        else:
            self.load_game()

    def new_game(self):
        """
        Initialises a new game.
        Shows a username prompt and handles user input.
        Generates a new game id and creates a new Player object with default 
        values. Afterwards starts the game.
        """
        while True:
            new_page(None, *Text.USERNAME)
            self.username = valid_string_input(
                "Please enter your username: ", 3, 15
            )
            if valid_confirm_input(f"Are you happy with {self.username}?: "):
                break
          
        while True:
            self.id = "".join(choice(ascii_uppercase) for i in range(6))
            if self.games_sheet.find(self.id) is None:
                break
        new_page(None, *Text.game_id(self.id))
        press_enter()

        new_page(None, *Text.STORYLINE)
        self.player = Player(self)
        self.save_game(False)
        press_enter()

        self.play_game()

    def load_game(self):
        """
        Initialises an existing game.
        Shows a game id prompt and handles user input.
        If a valid game id was entered, loads the game data and creates a new
        Player object with the loaded data.
        Afterwards starts the game.
        """
        while True:
            prev_id = valid_string_input("Please enter your game ID: ", 6, 6)
            prev_game = self.games_sheet.find(prev_id.upper())
            if prev_game is None:
                print_error("Could not find any game with this ID")
                if not valid_confirm_input("Would you like to try again?: "):
                    return
            else:
                data = self.games_sheet.row_values(prev_game.row)
                if int(data[3]) >= 60:
                    print_error("This game is already finished.")
                    if not valid_confirm_input(
                        "Would you like to try again?: "
                    ):
                        return
                else:
                    break
        if prev_game is None:
            return

        data = [
            int(value) if index > 1 else value
            for index, value in enumerate(data)
        ]
        self.id = data[0]
        self.username = data[1]
        new_page(None)
        print(colored_string(Colors.yellow, "Loading..."))
        self.player = Player(
            self,
            data[2],
            data[3],
            [data[i] for i in range(5, 10)],
            data[4],
            [data[i] for i in range(10, 15)],
        )
        self.play_game()

    def save_game(self, update=True):
        """
        Retrieves the progress from the Player object and saves it to Google
        sheets.
        """
        game_data = [self.id, self.username, *self.player.get_progress()]
        if update:
            prev_game = self.games_sheet.find(self.id)
            row = prev_game.row
            self.games_sheet.update(f"c{row}:o{row}", [game_data[2:]])
        else:
            self.games_sheet.append_row(game_data)

    def play_game(self):
        """
        Runs the game.
        If the game finishes successfully, the game results screen is shown.
        """
        if self.player.prepare_next_season():
            self.show_game_results()

    def show_game_results(self):
        """
        Shows the game result screen with the data from the current game.
        """
        new_page(None, *Text.end_screen(self))
        press_enter()
