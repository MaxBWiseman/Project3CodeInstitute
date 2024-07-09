import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("PythonFitnessConsole")

WORKOUTS = SHEET.worksheet("Workouts")
REPETITIONS = SHEET.worksheet("Repetitions")

BACK = WORKOUTS.col_values(1)
ARMS = WORKOUTS.col_values(2)
CHEST = WORKOUTS.col_values(3)
SHOULDERS = WORKOUTS.col_values(4)
LEGS = WORKOUTS.col_values(5)
print(value)



