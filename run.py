import gspread
from google.oauth2.service_account import Credentials
from src.game import Game

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("veggie_garden")

games_sheet = SHEET.worksheet("games")

print("Welcome to Veggie Garden, your own space to grow, harvest and sell vegetables!")
print("1: New Game")
print("2: Resume Game")
valid_input = False
while not valid_input:
    user_input = input("What would you like to do? (1 or 2): ")
    if user_input == "1" or user_input == "2":
        valid_input = True
    else:
        print("Invalid input. Please choose 1 or 2.")

if user_input == "1":
    game = Game(games_sheet, True)
else:
    game = Game(games_sheet, False)

