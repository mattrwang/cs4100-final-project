""" hill_descent_tests.py
Tests for hill descent functions.
"""
from WeekPlan import WeekPlan
from input_parser import input_parser
from hill_descent import HILLDESCENT, HILLDESCENT_RANDOM_UPHILL, energy_function, swap_tasks
from task import Task
import numpy as np

def test_energy_function():
    plan = np.array([0,0,0,-1,-1,-1,1,1,1,0,0,-2,2,2])
    groceries = Task('groceries', 3, 0.5, '647 Washington St, Newton, MA, 02458', ['sun', 10.0, 10.5], 'driving')
    work_cafe = Task('work', 4, 1.0, '1334 Boylston Street, Boston, MA 02215', ['sun', 12.0, 13.0], 'walking')
    tasks = [groceries, work_cafe]

    actual_total_energy = 3*3/12+3*3/12+5/12+2*4/12
    assert actual_total_energy == energy_function(plan, tasks)
test_energy_function()

def test_swap_tasks():
    pass
test_swap_tasks()

# plan = np.array([[0,0,0,0,0,0,2,0,0,0,3,0,0],
#                  [0,0,0,0,1,0,0,0,0,0,4,0,0]])
# groceries = Task('groceries', 3, 0.083, '647 Washington St, Newton, MA, 02458', 'driving')
# work_cafe = Task('work', 4, 0.083, '1334 Boylston Street, Boston, MA 02215', 'driving')
# t3 = Task('3', 3, 0.083, '647 Washington St, Newton, MA, 02458', 'driving')
# t4 = Task('4', 4, 0.083, '1334 Boylston Street, Boston, MA 02215', 'driving')
# tasks = [groceries, work_cafe, t3, t4]
# week_plan = WeekPlan('647 Washington St, Newton, MA, 02458', tasks)
# _, s = swap_tasks(1, 2, plan, week_plan)
# print(_, s)

tasks = input_parser("backend/day_planner/sample_tasks/task_set_C.csv")
week_plan = WeekPlan('34 Halcyon Rd, Newton Centre, MA, 02459', tasks)
plan = week_plan.generate_random_plan(tasks)
print(HILLDESCENT_RANDOM_UPHILL(10, plan, week_plan, 0.10))