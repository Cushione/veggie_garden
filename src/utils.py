import gspread
from google.oauth2.service_account import Credentials
from enum import Enum

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
