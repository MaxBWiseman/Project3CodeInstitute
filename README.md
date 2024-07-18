# The Python Fitness Console
![A muscular python](assets/images/editedbuffpython.png)
***
The Python Fitness Console is for every gym lover who like to track there progress and have a interactive console that increases repititons and weights set by the user automatically every week inline with muslce growth. The program works by understanding if the user had already used one of the 5 muslce groups before, if its the first time the program will ask the user what are their desired starting weights and repetitions they would like, and then saves this information in a google sheet. When a week has passed and the program detects this with "datetime" the reps and weights are incremented.

This is the *[Live version of my project](https://pythonfitnessconsole-3375f331b895.herokuapp.com/)*.

## Features
***

Included workouts:

1. Back
    1. Rear Delt Flys
    2. Lat Pulldowns
    3. Seated Rows
    4. Assisted Pull-Up
    5. Back Extension
2. Arms
    1. Bicep Curls
    2. Seated Dips
    3. Rope Pulldowns
    4. Rope Pullups
    5. Tricep Extension
3. Chest
    1. Chest Press
    2. Chest Flys(high)
    3. Seated Dips
    4. Chest Flys(low)
    5. Pec Deck
4. Shoulders
    1. Shoulder Press
    2. Lateral Raise
    3. Front Raise
    4. Rear Delt Row
    5. Arnold Press
5. Legs
    1. Squat Rack
    2. Leg Extensions
    3. Leg Curls
    4. Calf Raises
    5. Leg Press

#### Walkthrough

![Python Fitness Console Startup screen asking user what muscle group they would like to choose](assets/images/pfcss1.png)

 Asks the user what muscle group they would like to train today, chosen by entering the corresponding index number.

 Sets the current date in the background and saves it inside G16 in Repetitions in the google sheet.

![Python Fitness Console asking the user for desired weights and repetitions](assets/images/pfcss2.png)

![Python Fitness Console asking the user for desired weights and repetitions whilst iterating](assets/images/pfcss3.png)

 The console checks the linked google sheet wether or not the user has selected this muscle group before, if not it asks the user for weight and rep inputs.

![Python Fitness Console showing the user there selected workouts](assets/images/pfcss4.png)

 If the user has already selected the muscle group before and selected there desired reps and weights, the program will check wether or not a week has elapsed in time, if true then weights and reps are increased slowly automatically inline with muscle growth.Seen below.

 If not true then the program lets the user know and shows them their previously selected inputs. Seen above.


![Python Fitness Console incrementing the weights and reps automatically after a week has elapsed](assets/images/pfcss5.png)

The default setting for incrementing weights is 25%, and the repetitions are increased by 2. A prompt to let the user adjust this is a good idea for a new feature.


