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








def grab_exercises(data):
#using data to grab the correct exercises from the google sheet
    exercises = WORKOUTS.col_values(data)
#skip column name
    exercises = exercises[1:]
    print(f"Exercises for {WORKOUTS.cell(1, data).value}:")
#simple loop for iteration
    for exercise in exercises:
        print(exercise)







def welcome():
#Grab the workout names from the google sheet and store them in a variable
    workout_names = WORKOUTS.row_values(1)
    print("Welcome to the Python Fitness Console!\n")
    print("Please select a muscle group from the options below:\n")
# show workout options from google sheets, enumerate function is used to show the index of the list
    for i, workout in enumerate(workout_names, start=1):
        print(f"{i}. {workout}")
#Obtain user disision
    user_input = int(input("Enter the number of the muscle group you would like to do:\n "))
#this line checks the user_input is within the range of the workout_names list, valid range is 1 to the length of the list
    if 1 <= user_input <= len(workout_names):
        print(f"Great! You have selected the {workout_names[user_input-1]} muscle group.")
        grab_exercises(user_input)
    else:
        print("Invalid input. Please try again.")
