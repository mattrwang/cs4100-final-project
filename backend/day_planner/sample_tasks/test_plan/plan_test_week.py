from WeekPlan import WeekPlan
from input_parser import input_parser
from hill_descent import *
from Task import Task
import numpy as np


tasks = input_parser("nadya_input_sample.csv")
week_plan = WeekPlan("1274 Beacon St, Newton, MA, 02468", tasks, day_start_time=9.0, day_end_time=21.0)

plan = week_plan.generate_random_plan(tasks)
best_plan, best_energy = HILLDESCENT_RANDOM_RESTART(2, 50, plan, week_plan)
print(best_plan)
print(best_energy)

