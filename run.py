import logging
import gspread
from google.oauth2.service_account import Credentials
import gspread.utils
from gspread.exceptions import GSpreadException
import datetime

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

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
WEIGHTS = SHEET.worksheet("Weights")

def grab_exercises(data):
    #using data to grab the correct exercises from the google sheet
    #skips the first row as it is the title
    try:
        data = int(data)  # Ensure data is an integer
        if not 1 <= data <= WORKOUTS.col_count:  # Assuming WORKOUTS.col_count gives the number of columns
            raise ValueError("Invalid column index.")
        exercises = WORKOUTS.col_values(data)[1:]
        print(f"Exercises for {WORKOUTS.cell(1, data).value}:\n")
        #using the get_repetitions function to grab the repetitions for the exercises
        repetitions, weights = get_repetitions_weights(data, len(exercises), exercises)
        #using the zip function to combine the exercises and repetitions into a single list
        for exercise, rep, weight in zip(exercises, repetitions, weights):
            print(f"{exercise} - {rep} repetitions - {weight} kg\n")
        # Message to the user after displaying the exercises
        print("Please click run program again when you start another session, your choices if picked before will be remembered and incremented slowly over the course of a week.")
    except ValueError as e:
        print(f"Error: {e}")

def welcome():
    try:  # Correctly indented try block
        workout_names = WORKOUTS.row_values(1)
        print("Welcome to the Python Fitness Console!\n")
        print("Please select a muscle group from the options below:\n")
        # Show workout options from Google Sheets, enumerate function is used to show the index of the list
        for i, workout in enumerate(workout_names, start=1):
            print(f"{i}. {workout}")
        # Obtain user decision
        user_input = int(input("Enter the number of the muscle group you would like to do:\n "))
        # This line checks the user_input is within the range of the workout_names list, valid range is 1 to the length of the list
        if 1 <= user_input <= len(workout_names):
            print(f"Great! You have selected the {workout_names[user_input-1]} muscle group.\n")
            # Grab the exercises for the user_input
            grab_exercises(user_input)
        else:
            print("Invalid input. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")
            
def get_repetitions_weights(column_index, number_of_exercises, exercise_names):
#Cell where data will be stored
    last_update_cell = 'G16'
#Grab the last updated date from the google sheet
    last_updated_str = SHEET.worksheet("Repetitions").acell(last_update_cell).value
#Adjust current_date for testing, checking if the weights and reps are being increased when a week has passed with this code-
#datetime.datetime.strptime("2024-07-22", "%Y-%m-%d").date()
#Adjust the inner date to test the code    
    current_date = datetime.date.today()
    
#If the date is empty, update the google sheet with the current date
    if not last_updated_str:
        SHEET.worksheet("Repetitions").update_acell(last_update_cell, current_date.strftime("%Y-%m-%d"))
        last_updated = current_date
    else:
        #string to date
        last_updated = datetime.datetime.strptime(last_updated_str, "%Y-%m-%d").date()
    
    reps = [int(rep) for rep in REPETITIONS.col_values(column_index)[1:]]
    weights = [int(weight) for weight in WEIGHTS.col_values(column_index)[1:]]
    
#Check if the last update was more than a week ago or first time for muscle group
    if (current_date - last_updated).days >= 7:
        print("More than a week has passed. Increasing workout intensity!\n")
        #if reps already set, increment reps to simulate muscle growth
        reps = [int(rep) + 2 for rep in REPETITIONS.col_values(column_index)[1:]] # increase in reps
#if weights already set, increment weights to simulate muscle growth
        weights = [int(weight) + int(weight) * 1.25 for weight in WEIGHTS.col_values(column_index)[1:]] #  increase in weight
#update the google sheet with the new reps and weights
        update_rep_sheet(column_index, reps)
        update_weight_sheet(column_index, weights)
        REPETITIONS.update_acell(last_update_cell, current_date.strftime("%Y-%m-%d"))
    elif not reps or len(reps) < number_of_exercises:
#Check if the reps are empty, less than the number of exercises or last updated more than a week ago
        print("It's time to update your workout intensity or set up your initial workout plan!\n")
#loop through the exercises and ask for reps and weights
        for exercise_name in exercise_names:
            rep = int(input(f"Enter the number of repetitions for {exercise_name}:\n"))
            weight = int(input(f"Enter the weight for {exercise_name} in kg:\n"))
#append reps and weights to the lists
            reps.append(rep)
            weights.append(weight)
#update the google sheet with the reps and weights
        update_rep_sheet(column_index, reps)
        update_weight_sheet(column_index, weights)
        REPETITIONS.update_acell(last_update_cell, current_date.strftime("%Y-%m-%d"))
    else:
        print("Less than a week has passsed. Your workout intensity is up to date!\n")

    return reps, weights
            
#I asked microsoft co pilot for help with this function, it suggested the following code (had to refactor as code did not fully work)
"""
    issue was how the range_to_update string is constructed, it seems that REPETITIONS.
    title might already include the sheet name and appending it again with ! causes the
    malformed string, also there was a update to the gspread "update()" function where i
    had to swap around my "range_to_update" and "values_to_update" variables on line 88
"""
def update_rep_sheet(column_index, reps):
    try:
    #Convert column index to corresponding A1 notation column letter
        column_letter = gspread.utils.rowcol_to_a1(1, column_index)[0]
     # Prepare the range string for the update, e.g. "A2:A5"
        range_to_update = f"{column_letter}2:{column_letter}{1 + len(reps)}"
    # Prepare the data in the format expected by the update method (list of lists)
        values_to_update = [[rep] for rep in reps]
    # Update the sheet
        REPETITIONS.update(values_to_update, range_to_update)
    #I learned from this what rowcol_to_a1 does from gspread
    #I discovered about the logging module from this page after searching "how to log errors in python"
    #https://stackoverflow.com/questions/4508849/how-to-log-python-exception
    except GSpreadException as e:
        logging.error(f"Failed to update the Repetitions sheet: {e}")
    except Exception as e:
        logging.error(f"An error occurred whilst updating: {e}")
    
#copied last function and changed slighty to update the weights sheet instead
def update_weight_sheet(column_index, weights):
    try:
    #Convert column index to corresponding A1 notation column letter
        column_letter = gspread.utils.rowcol_to_a1(1, column_index)[0]
     # Prepare the range string for the update, e.g. "A2:A5"
        range_to_update = f"{column_letter}2:{column_letter}{1 + len(weights)}"
    # Prepare the data in the format expected by the update method (list of lists)
        values_to_update = [[weights] for weights in weights]
    # Update the sheet
        WEIGHTS.update(values_to_update, range_to_update)
    #I discovered about the logging module from this page after searching "how to log errors in python"
    #https://stackoverflow.com/questions/4508849/how-to-log-python-exception
    except GSpreadException as e:
        logging.error(f"Failed to update the Weights sheet: {e}")
    except Exception as e:
        logging.error(f"An error occurred whilst updating: {e}")
        
#My code wouldent start in console, after reasearch i found that my code doesnt automatically execute because the call is at global level.
#I then reasearched different ways to fix this problem and found this video https://www.youtube.com/watch?v=g_wlZ9IhbTs - at 2:37 he explains how to fix this problem
if __name__ == "__main__":
    welcome()