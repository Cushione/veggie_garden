import gspread
from google.oauth2.service_account import Credentials
import os
from textwrap import fill

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("veggie_garden")


crops_sheet = SHEET.worksheet("crops")
CROPS = crops_sheet.col_values(1)[1:]

MONTHS = ["April", "May", "June", "July", "August", "September"]

def valid_number_input(prompt, minimum, maximum):
    while True:
        user_input = input(colored_string(Colors.yellow, f"\n{prompt}"))
        try:
            user_input = int(user_input.strip())
        except ValueError:
            print_error(f"Please type in a valid number ({minimum}-{maximum}).")
            continue
        if user_input >= minimum and user_input <= maximum:
            break
        else:
            print_error(f"Please type in a valid number ({minimum}-{maximum}).")
    return user_input

def valid_string_input(prompt, minimum, maximum):
    while True:
        user_input = input(colored_string(Colors.yellow, f"\n{prompt}")).strip()
        if len(user_input) >= minimum and len(user_input) <= maximum:
            break
        else:
            print_error(f"Please type in a valid string ({minimum}{f'-{maximum}' if maximum != minimum else ''} characters).")
    return user_input

def valid_confirm_input(prompt):
    while True:
        user_input = input(colored_string(Colors.yellow, f"\n{prompt}")).strip().lower()
        if user_input in ["yes", "y"]:
            result = True
            break
        elif user_input in ["no", "n"]:
            result = False
            break
        else:
            print_error("Please type either yes/y or no/n.")
    return result

def press_enter(prompt = "Press Enter to continue."):
    input(colored_string(Colors.yellow, f"\n{prompt}"))

def print_error(message):
    print(colored_string(Colors.red, message))


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def new_page(game, heading=None, *content):
    clear_terminal()
    username = f" - {game.username}" if game else ""
    game_id = f"ID: {colored_string(Colors.rgb(255, 165, 0), game.id)}" if game else ""
    season = f"Year {int((game.player.month / 6) + 1)}" if game else "" 
    money = f"€{game.player.money}" if game else ""
    title = colored_string(Colors.green, "Veggie Garden")
    print(f"{title} {game_id}{username.ljust(15)}  {colored_string(Colors.cyan, money.ljust(26))} {colored_string(Colors.green, season.rjust(9))}")
    print("-----------------------------------------------------------------------------\n")
    print(f"{colored_string(Colors.blue, heading.upper())}\n" if heading else "")
    for line in content:
        print(f"{fill(line, width=77)}\n")

# Learned how to add colors to the terminal at
# https://replit.com/talk/learn/ANSI-Escape-Codes-in-Python/22803
def colored_string(color, string):
    return f"{color}{string}{Colors.white}"

class Colors:
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"

    def rgb(r, g, b): 
        return f"\u001b[38;2;{r};{g};{b}m"

class Text:
    MAIN_MENU = (
        "Main Menu",
        "Welcome to Veggie Garden, your own space to grow, harvest, and sell "
        + "vegetables!",
        "This is a text based game. To control the game, type in either a "
        + "number for numbered options, or y(es)/n(o) to confirm actions.",
        "Please select one of the following options to continue:"
        )

    USERNAME = (
        "New Game",
        "Please select a username (3 - 20 characters)"
    )

    @staticmethod
    def game_id(g_id):
        return (
            "Game ID",
            f"Your game ID is: {g_id}",
            "Please write it down so you can resume your game again later."
        )

    FERTILISER = (
        "Fertiliser", 
        "Your compost is your source of fertiliser. Upgrage your compost pile to produce higher quality fertiliser." 
    )

    UPGRADE_FERTILISER = ("Upgrade Fertiliser")

    FIELDS = (
        "Fields",
        "Plant your crops here. Unlock more fields for greater harvest. "
    )

    UNLOCK_NEW_FIELD = (
        "Unlock new field",
        "Buy another field to increase your yield."
    )

    ASSIGN_CROPS = (
        "Assign Crops",
        "Assign crops to your fields. Be aware that each field can only have on type of crop on it."
    )

    AVAILABLE_SEEDS = (
        "Available Seeds"
    )

    PERPARE_SEASON = (
        "Prepare for the next Season",
        "New Season is about to start. Stock up on seeds and plant your fields."
    )

    STORAGE = (
        "Storage",
        "Available seeds for planting."
    )

    NEXT_SEASON = (
        "Start next season",
        "Next season is about to begin. Are you ready?"
    )

    SEASON_OVERVIEW = (
        "Season Overview"
    )

    STORE = (
        "Store",
        "Welcome to the local garden supply store. Buy your seeds here."
    )
    
    @staticmethod
    def end_screen(game):
        return (
            "Congratulations!",
            f"You have finished the game with €{game.player.money}!",
            "Go to Highscores to find out if you made it on the list."
        )
    SAVE_EXIT = (
        "Save and exit?",
        "Remember your game ID to come back later!"
    )