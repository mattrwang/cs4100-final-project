from WeekPlan import WeekPlan
from input_parser import input_parser
from hill_descent import HILLDESCENT, energy_function, swap_tasks
from Task import Task
import numpy as np

def test_energy_function():
    plan = np.array([0,0,0,-1,-1,-1,1,1,1,0,0,-2,2,2])
    groceries = Task('groceries', 3, 0.5, '647 Washington St, Newton, MA, 02458', ['sun', 10.0, 10.5], 'driving')
    work_cafe = Task('work', 4, 1.0, '1334 Boylston Street, Boston, MA 02215', ['sun', 12.0, 13.0], 'walking')
    tasks = [groceries, work_cafe]

    actual_total_energy = 3*3/12+3*3/12+5/12+2*4/12
    assert actual_total_energy == energy_function(plan, tasks)
test_energy_function()

tasks = input_parser("backend/day_planner/sample_input.csv")
week_plan = WeekPlan("Davenport Commons B, 696 Columbus Ave, Boston, MA 02118", tasks)
plan = week_plan.generate_random_plan(tasks)
print(plan)
result = HILLDESCENT(1000, plan, week_plan)
print(result)