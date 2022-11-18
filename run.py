"""
    Main module
    Entry file for the application. 
"""

from src.game import Game
from src.utils import (
    valid_number_input,
    new_page,
    Text,
    press_enter,
    get_highscores,
)

while True:
    new_page(None, *Text.MAIN_MENU)

    print("1: New Game")
    print("2: Resume Game")
    print("3: Highscores")
    print("4: How to Play")
    print("0: Exit Game")
    user_input = valid_number_input("What would you like to do?: ", 0, 4)

    if user_input == 1:
        game = Game(True)
    elif user_input == 2:
        game = Game(False)
    elif user_input == 3:
        new_page(None, Text.HIGHSCORES)
        for index, game in enumerate(get_highscores()):
            print(
                f"{str(index + 1).rjust(3)}.  {game[1].ljust(15)}  €{game[2]}"
            )
        press_enter()
    elif user_input == 4:
        new_page(None, *Text.HOW_TO_PLAY)
        press_enter()
    else:
        new_page(None, *Text.EXIT)
        break
