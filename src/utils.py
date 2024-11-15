"""
Utils Module.
A collection of shared constants and functions that are shared by other 
modules. 
"""
import gspread
from google.oauth2.service_account import Credentials
import os
from textwrap import fill

# Google Sheet Initialisation and Authorisation
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("veggie_garden")

# List of Crop Names
crops_sheet = SHEET.worksheet("crops")
CROPS = crops_sheet.col_values(1)[1:]

# List of relevant month names
MONTHS = ["April", "May", "June", "July", "August", "September"]


def valid_number_input(prompt, minimum, maximum):
    """
    Requests a number from the user.
    Validates the input to ensure that a valid number from the given range
    is entered.
    """
    while True:
        user_input = input(colored_string(Colors.yellow, f"\n{prompt}"))
        # Validate that input is a valid integer number
        try:
            user_input = int(user_input.strip())
        except ValueError:
            print_error(
                f"Please type in a valid number ({minimum}-{maximum})."
            )
            continue
        # Validate that number is between minimum and maximum value 
        if user_input >= minimum and user_input <= maximum:
            break
        else:
            print_error(
                f"Please type in a valid number ({minimum}-{maximum})."
            )
    # Return the valid number input
    return user_input


def valid_string_input(prompt, minimum, maximum):
    """
    Requests a string from the user.
    Validates the input to ensure that a valid string with a valid length
    is entered.
    """
    while True:
        user_input = input(
            colored_string(Colors.yellow, f"\n{prompt}")
        ).strip()
        # Validate that the string has a valid length
        if len(user_input) >= minimum and len(user_input) <= maximum:
            break
        else:
            print_error(
                f"Please type in a valid string ({minimum}"
                + f"{f'-{maximum}' if maximum != minimum else ''} characters)."
            )
    # Return the valid user input
    return user_input


def valid_confirm_input(prompt):
    """
    Requests a confirmation from the user.
    Validates the input to ensure that a valid confirmation is entered.
    """
    while True:
        user_input = (
            input(colored_string(Colors.yellow, f"\n{prompt}")).strip().lower()
        )
        # Validate that either y(es) or n(o) was entered
        if user_input in ["yes", "y"]:
            result = True
            break
        elif user_input in ["no", "n"]:
            result = False
            break
        else:
            print_error("Please type either yes/y or no/n.")
    # Return the valid user input
    return result


def press_enter(prompt="Press Enter to continue."):
    """
    Prompts the user to press Enter.
    """
    input(colored_string(Colors.yellow, f"\n{prompt}"))


def print_error(message):
    """
    Prints a message as an error.
    """
    print(colored_string(Colors.red, message))


def clear_terminal():
    """
    Clears the terminal.
    """
    # Clear the terminal by calling the OS specific command
    os.system("cls" if os.name == "nt" else "clear")


def new_page(game, heading=None, *content):
    """
    Displays a new page by clearing the terminal and then printing the
    standard elements with the given text and data.
    """
    clear_terminal()
    # Prepare data for the header
    username = f" - {game.username}" if game else ""
    game_id = (
        f"ID: {colored_string(Colors.rgb(255, 165, 0), game.id)}"
        if game
        else ""
    )
    if game:
        year = (
            int((game.player.month / 6) + 1)
            if game.player.month < 60
            else "10"
        )
        season = f"Year {year}"
    else:
        season = ""
    money = f"€{game.player.money}" if game else ""
    title = colored_string(Colors.green, "Veggie Garden")
    # Print header with data
    print(
        f"\n{title} {game_id}{username.ljust(15)}  "
        + f"{colored_string(Colors.cyan, money.ljust(26))} "
        + f"{colored_string(Colors.green, season.rjust(9))}"
    )
    # Print line underneath the header
    print(f"{''.join(['-' for i in range(77)])}\n")
    # Print heading if provided
    if heading:
        print(
            f"{colored_string(Colors.blue, heading.upper())}\n"
        )
    # Print all the provided content
    for line in content:
        print(f"{fill(line, width=77)}\n")


def get_highscores():
    """
    Returns the ten best finished games
    """
    # Load all the games without name row
    games_sheet = SHEET.worksheet("games")
    games_data = games_sheet.get_all_values()[1:]
    # Filter finished games
    finished_games = [row for row in games_data if int(row[3]) == 60]
    # Sort games by money in descending order
    finished_games.sort(key=lambda game: int(game[2]), reverse=True)
    # Return the first 10 games
    return finished_games[:10]


# Learned how to add colors to the terminal at
# https://replit.com/talk/learn/ANSI-Escape-Codes-in-Python/22803

def colored_string(color, string):
    """
    Returns the given string in the given color.
    """
    return f"{color}{string}{Colors.white}"


class Colors:
    """
    Holds colors as ANSI Escape Codes.
    Used for coloring of text in the terminal.
    """
    black = "\u001b[30m"
    red = "\u001b[31m"
    green = "\u001b[32m"
    yellow = "\u001b[33m"
    blue = "\u001b[34m"
    magenta = "\u001b[35m"
    cyan = "\u001b[36m"
    white = "\u001b[37m"

    @staticmethod
    def rgb(red, green, blue):
        """
        Returns the ANSI Escape code for coloring a string with the
        given red, green and blue values
        """
        return f"\u001b[38;2;{red};{green};{blue}m"


class Text:
    """
    Holds text for the heading and description for every page.
    """
    MAIN_MENU = (
        "Main Menu",
        "Welcome to Veggie Garden, your own space to grow, harvest, and sell "
        + "vegetables!",
        "This is a text based game. To control the game, type in either a "
        + "number for numbered options, or y(es)/n(o) to confirm actions.",
        "Please select one of the following options to continue:",
    )

    USERNAME = ("New Game", "Please select a username (3 - 15 characters)")

    @staticmethod
    def game_id(g_id):
        id_string = colored_string(Colors.rgb(255, 165, 0), g_id)
        return (
            "Game ID",
            f"Your game ID is: {id_string}",
            "Please write your game ID down so you can resume your "
            + "game again later.",
        )

    FERTILISER = (
        "Fertiliser",
        "Your compost is your source of fertiliser. Upgrage your compost "
        + "pile to produce higher quality fertiliser.",
    )

    UPGRADE_FERTILISER = "Upgrade Fertiliser"

    FIELDS = (
        "Fields",
        "Plant your crops here. Unlock more fields for greater harvest. ",
    )

    UNLOCK_NEW_FIELD = (
        "Unlock new field",
        "Buy another field to increase your yield.",
    )

    ASSIGN_CROPS = (
        "Assign Crops",
        "Assign crops to your fields. Be aware that each field can only "
        + "have 1 type of crop on it.",
    )

    AVAILABLE_SEEDS = "Available Seeds"

    @staticmethod
    def prepare_season(month):
        return (
            "Prepare Season",
            "New Season is about to start. Stock up on seeds and plant "
            + "your fields."
            if month < 54
            else "This is your final season!",
        )

    STORAGE = ("Storage", "Available seeds for planting.")

    NEXT_SEASON = (
        "Start next season",
        "Next growing season is about to begin. Have you planted your seeds?",
    )

    SEASON_OVERVIEW = "Season Overview"

    STORE = (
        "Store",
        "Welcome to the local garden supply store. Buy your seeds here.",
    )

    @staticmethod
    def end_screen(game):
        return (
            "Congratulations!",
            f"You have finished the game with €{game.player.money}!",
            "Go to High Scores to find out if you made it on the list.",
        )

    HOW_TO_PLAY = (
        "How to play",
        "Main Objective: You have 10 years to cultivate your veggie garden "
        + "and earn as much money as possible.",
        "Seasons: Each year consists of 6 growing months (April - September)."
        + "\nStock up on your seeds before the season starts, once the season "
        + "is in progress, you cannot buy new seeds anymore.",
        "Vegetables: All vegetables have different growing time, so you need "
        + "to experiment with your seeds and observe their progress on "
        + "monthly basis.",
        "Fields: Each field is for one type of vegetable only. If you "
        + "decide to assign another crop to the field, the previous seed is "
        + "lost and replaced by the new seed.",
        "Fertiliser: There are various types of fertiliser for boosting your "
        + "seasonal yield. Level up for more profit.",
        "Store: The local store is the perfect place to stock up on your "
        + "seeds and exchange farm gossip.",
        "Storage: A place to keep your seeds safe.",
        "Special Events: Be aware of different types of natural hazards. "
        + "There is nothing you can do about them, nature is unpredictable.",
    )

    HIGHSCORES = "High Scores"

    SAVE_EXIT = ("Save and exit?", "Remember your game ID to come back later!")

    EXIT = ("goodbye", "Thank you for playing, see you soon!")

    STORYLINE = (
        "Storyline",
        "You have inherited a field from your grandfather, together with €20. "
        + "Your dream of starting your own veggie garden has come true!",
        "Now you can buy and plant seeds, harvest the crops when they are "
        + "ready, and finally, sell them for profit. Every crop has a "
        + "different growing time and brings different reward.",
        "Unlock new fields to maximise your growing potential, apply "
        + "fertiliser to grow bigger vegetables, and watch your garden "
        + "blossom.",
        "Have fun!",
    )
