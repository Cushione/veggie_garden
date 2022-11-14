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

special_events = SHEET.worksheet("special_events")
print(special_events.get_values())

games_sheet = SHEET.worksheet("games")
username = input("Please enter your username: ")
game = Game(username, games_sheet)

