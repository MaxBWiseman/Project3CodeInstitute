import gspread
from google.oauth2.service_account import Credentials
import gspread.utils


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






def grab_exercises(data):
#using data to grab the correct exercises from the google sheet
    exercises = WORKOUTS.col_values(data)[1:]
    print(f"Exercises for {WORKOUTS.cell(1, data).value}:\n")
#using the get_repetitions function to grab the repetitions for the exercises
    repetitions = get_repetitions(data, len(exercises), exercises)
#using the zip function to combine the exercises and repetitions into a single list
    for exercise, rep in zip(exercises, repetitions):
        print(f"{exercise} - {rep} repetitions")
    

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
        print(f"Great! You have selected the {workout_names[user_input-1]} muscle group.\n")
        grab_exercises(user_input)
    else:
        print("Invalid input. Please try again.")
        

def get_repetitions(column_index, number_of_reps, exercise_names):
#check if already set reps once
    reps = REPETITIONS.col_values(column_index)[1:]
    if not reps or len(reps) < number_of_reps:
#if first time or no data, ask for reps   
        reps = []
        for i in range(number_of_reps):
            initial_rep = int(input(f"Enter the number of repetitions for exercise {i+1}:\n"))
            reps.append(initial_rep)
        #update the google sheet with the reps
        update_rep_sheet(column_index, reps)
    else:
        #if reps already set, increment reps to simulate muscle growth
        reps = [int(rep) + 1 for rep in reps]
        update_rep_sheet(column_index, reps)
    return reps
            
            
            
#I asked microsoft co pilot for help with this function, it suggested the following code (had to refactor as code did not fully work)
    """
    issue was how the range_to_update string is constructed, it seems that REPETITIONS.
    title might already include the sheet name and appending it again with ! causes the
    malformed string, also there was a update to the gspread "update()" function where i
    had to swap around my "range_to_update" and "values_to_update" variables on line 88
    """
def update_rep_sheet(column_index, reps):
#Convert column index to corresponding A1 notation column letter
    column_letter = gspread.utils.rowcol_to_a1(1, column_index)[0]
     # Prepare the range string for the update, e.g. "A2:A5"
    range_to_update = f"{column_letter}2:{column_letter}{1 + len(reps)}"
    # Prepare the data in the format expected by the update method (list of lists)
    values_to_update = [[rep] for rep in reps]
    # Update the sheet
    REPETITIONS.update(values_to_update, range_to_update)
#I learned from this what rowcol_to_a1 does from gspread


#My code wouldent start in console, after reasearch i found that my code doesnt automatically execute because the call is at global level.
#I then reasearched different ways to fix this problem and found this video https://www.youtube.com/watch?v=g_wlZ9IhbTs - at 2:37 he explains how to fix this problem
if __name__ == "__main__":
    welcome()