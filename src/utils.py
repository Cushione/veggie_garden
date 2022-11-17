import gspread
from google.oauth2.service_account import Credentials
from enum import Enum
import os

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
        user_input = input(prompt)
        try:
            user_input = int(user_input.strip())
        except ValueError:
            print(f"Please type in a valid number ({minimum}-{maximum}).")
            continue
        if user_input >= minimum and user_input <= maximum:
            break
        else:
            print(f"Please type in a valid number ({minimum}-{maximum}).")
    return user_input

def valid_string_input(prompt, minimum, maximum):
    while True:
        user_input = input(prompt).strip()
        if len(user_input) >= minimum and len(user_input) <= maximum:
            break
        else:
            print(f"Please type in a valid string ({minimum}-{maximum} characters).")
    return user_input

def valid_confirm_input(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ["yes", "y"]:
            result = True
            break
        elif user_input in ["no", "n"]:
            result = False
            break
        else:
            print("Please type either yes/y or no/n.")
    return result

def press_enter():
    input("Press Enter to continue.")


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def new_page(game):
    clear_terminal()
    username = f" - {game.username}" if game else ""
    game_id = f"ID: {game.id}" if game else ""
    season = f"Year {int((game.player.month / 6) + 1)}" if game else "" 
    money = f"€{game.player.money}" if game else ""
    print(f"Veggie Garden {game_id.ljust(9)}{username.ljust(15)} {money.rjust(27)} {season.rjust(9)}")
    print("-----------------------------------------------------------------------------\n")
