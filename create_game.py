
import pandas as pd
import numpy as np
import random


'''
Each hole will consist of 3 shots; Drive, Approach, Chip.
A randomly generated yardage will be generated for each hole, followed by shots.
'''

holes = 18

driver_goal = 280

par_four_range = (320, 460)
par_five_range = (461, 580)
par_three_range = (140, 220)

hole_number = [f"hole_{x}" for x in range(1, holes+1)]
par_list = [5]*2 + [3]*2 + [4]*5

course_list = []

# Generate course base on number of holes
if holes == 18:

    random.shuffle(par_list)
    front_nine = par_list.copy()

    random.shuffle(par_list)
    back_nine = par_list.copy()

    course = front_nine + back_nine

elif holes == 9:

    random.shuffle(par_list)
    course = par_list.copy()

elif holes < 9:
    course = random.choices(par_list, k=holes)

else:
    course = random.choices(par_list*2, k=holes)


for hole, par in zip(hole_number, course):

    # Generate hole length
    if par == 3:
        yards = random.choice(range(par_three_range[0],
                                    par_three_range[1]))

    if par == 4:
        yards = random.choice(range(par_four_range[0],
                                    par_four_range[1]))

    if par == 5:
        yards = random.choice(range(par_five_range[0],
                                    par_five_range[1]))

    # Calculate approach and chip shot lengths
    approach = yards - driver_goal
    chip_pitch = random.choice(range(5, 20))

    # Add hole info to temp dictionary
    temp_dict = {}

    temp_dict['hole'] = hole
    temp_dict['par'] = par
    temp_dict['yards'] = yards
    temp_dict['drive_g'] = driver_goal
    temp_dict['appch_g'] = approach
    temp_dict['chip_pitch_g'] = chip_pitch

    # add hole to final list
    course_list.append(temp_dict)

game_df =  pd.DataFrame(course_list)
