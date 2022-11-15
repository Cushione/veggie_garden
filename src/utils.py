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
crop_names = crops_sheet.col_values(1)
CROPS = Enum("CROPS", crop_names)