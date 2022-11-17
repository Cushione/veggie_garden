from src.game import Game
from src.utils import valid_number_input, new_page, Text

while True:
    new_page(None, *Text.MAIN_MENU)

    print("1: New Game")
    print("2: Resume Game")
    user_input = valid_number_input("What would you like to do?: ", 1, 2)

    if user_input == 1:
        game = Game(True)
    else:
        game = Game(False)

