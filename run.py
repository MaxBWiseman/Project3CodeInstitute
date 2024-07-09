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

def welcome():
#Grab the workout names from the google sheet
    workout_names = WORKOUTS.row_values(1)
    print("Welcome to the Python Fitness Console!\n")
    print("Please select a workout from the options below:\n")
# show workout options from google sheets
    for i, workout in enumerate(workout_names, start=1):
        print(f"{i}. {workout}")
#Obtain user disision
user_input = int(input("Enter the number of the workout you would like to do:\n "))
#select the workout
if user_input == 1:
    print(f"Great! You have selected the {BACK[user_input]} workout.")
elif user_input == 2:
    print(f"Great! You have selected the {ARMS[user_input]} workout.")
elif user_input == 3:
    print(f"Great! You have selected the {CHEST[user_input]} workout.")
elif user_input == 4:
    print(f"Great! You have selected the {SHOULDERS[user_input]} workout.")
elif user_input == 5:
    print(f"Great! You have selected the {LEGS[user_input]} workout.")
else:
    print("Invalid input. Please try again.")
    
       
welcome()
    




