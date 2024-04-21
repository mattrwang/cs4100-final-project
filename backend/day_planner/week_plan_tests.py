""" week_plan_tests.py
Tests for functions in the WeekPlan class.
"""

from WeekPlan import WeekPlan
from task import Task
import numpy as np

def test_add_task_to_day():
     # case 1: adding a task between two tasks that requires changing transportation time before and after task
    day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                        1,1,1,1,1,1,0,0,0,0,0,0, 
                        0,0,0,0,0,0,0,0,0,0,0,0,
                        2,2,2,2,2,2,2,2,2,2,2,2])
    home = '34 Halcyon Rd, Newton Centre, MA, 02459'
    groceries = Task('groceries', 3, 0.5, '647 Washington St, Newton, MA, 02458', ['Sunday', 10.0, 10.5], 'driving')
    work_cafe = Task('work cafe', 4, 1.0, '1334 Boylston Street, Boston, MA 02215', ['Sunday', 12.0, 13.0], 'driving')
    walk_park = Task('walk in park', 2, 0.416666, '1094 Beacon St, Newton, MA 02461', None, 'driving')
    tasks = [groceries, work_cafe, walk_park]  
    week_plan = WeekPlan(home, tasks)
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 2, walk_park, 25, 30)
    actual_new_day_plan_google = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                        1,1,1,1,1,1,0,0,0,0,0,-3, 
                        -3,3,3,3,3,3,0,0,-2,-2,-2,-2,
                        2,2,2,2,2,2,2,2,2,2,2,2])
    actual_new_day_plan_est = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                        1,1,1,1,1,1,0,0,0,0,0,0, 
                        -3,3,3,3,3,3,0,0,0,0,-2,-2,
                        2,2,2,2,2,2,2,2,2,2,2,2])
    assert status == 1
    assert np.array_equiv(new_day_plan, actual_new_day_plan_est)

    # case 2: adding a task as the first/last task of the day before heading home in a location that is not home
    # first
    day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,2,2,2,2,2,2,2,2,2,2])
    actual_new_day_plan_google = np.array([-3,3,3,3,3,3,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,2,2,2,2,2,2,2,2,2,2])
    actual_new_day_plan_est = np.array([-3,3,3,3,3,3,0,0,0,0,0,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,2,2,2,2,2,2,2,2,2,2])
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 2, walk_park, 1, 6)
    assert status == 1
    assert np.array_equiv(new_day_plan, actual_new_day_plan_est)
   
    
    # last
    day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,0,0,0,0,0,0,0,0,0,0])
    groceries = Task('groceries', 3, 0.5, '647 Washington St, Newton, MA, 02458', ['Sunday', 10.0, 10.5], 'driving')
    work_cafe = Task('work cafe', 4, 0.166666, '1334 Boylston Street, Boston, MA 02215', ['Sunday', 12.0, 12.166666], 'driving')
    walk_park = Task('walk in park', 4, 0.33333, '1109 Beacon St, Newton, MA, 02459', None,'driving')

    tasks = [groceries, work_cafe, walk_park]
    actual_new_day_plan_google = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,0,-3,-3,-3,-3,3,3,3,3,-3])
    actual_new_day_plan_est = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,0,0,0,-3,-3,3,3,3,3,-3])
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 2, walk_park, 43, 47)
    assert status == 1
    assert np.array_equiv(new_day_plan, actual_new_day_plan_est)

    # case 3: adding a task that requires overwriting another task's alloted time (fail)
    day_plan = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    groceries = Task('groceries', 3, 1.0, None, ['sun', 9.0, 10.0], 'driving')
    walk_park = Task('walk in park', 4, 1.0, None, ['sun', 9.0, 10.0],'driving')
    tasks = [groceries, walk_park]
    actual_new_day_plan = day_plan
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 1, walk_park, 43, 47)
    assert status == 0
    assert np.array_equiv(new_day_plan, actual_new_day_plan)
test_add_task_to_day()

def test_generate_random_plan():
    home = '34 Halcyon Rd, Newton Centre, MA, 02459'
    groceries = Task('groceries', 3, 0.5, '647 Washington St, Newton, MA, 02458', ['Sunday', 10.0, 10.5], 'driving')
    work_cafe = Task('work cafe', 4, 1.0, '1334 Boylston Street, Boston, MA 02215', ['Sunday', None, None], 'driving')
    study_home = Task('study', 2, 0.416666, home, None, 'driving')
    tasks = [groceries, work_cafe, study_home]

    week_plan = WeekPlan(home, tasks)
    plan = week_plan.generate_random_plan(tasks)
    # check each task is in th eplan for the specified time intervals
    assert np.count_nonzero(plan == 1) == 6
    assert np.count_nonzero(plan == 2) == 12
    assert np.count_nonzero(plan == 3) == 5
test_generate_random_plan()

def test_valid_plan():
    # case 1: valid plan
    home = '34 Halcyon Rd, Newton Centre, MA, 02459'
    groceries = Task('groceries', 3, 0.5, '647 Washington St, Newton, MA, 02458', ['Sunday', 10.0, 10.5], 'driving')
    work_cafe = Task('work cafe', 4, 1.0, '1334 Boylston Street, Boston, MA 02215', ['Sunday', None, None], 'driving')
    study_home = Task('study', 2, 0.5, home, None, 'driving')
    tasks = [groceries, work_cafe, study_home]

    week_plan = WeekPlan(home, tasks)
    plan = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0]])
    assert week_plan.valid_day_tasks(plan)
    
    # case 2: missing one interval for task 3 (not valid)
    week_plan = WeekPlan(home, tasks)
    plan = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0]])
    assert week_plan.valid_day_tasks(plan)
test_valid_plan()


plan = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -2, -2, 2, 2, 2, 2,
        2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0]])

groceries = Task('groceries', 3, 0.5, '647 Washington St, Newton, MA, 02458', ['Sunday', 10.0, 10.5], 'driving')
work_cafe = Task('work cafe', 4, 1.0, '1334 Boylston Street, Boston, MA 02215', ['Sunday', None, None], 'driving')
study_home = Task('study', 2, 0.5, '34 Halcyon Rd, Newton Centre, MA, 02459', None, 'driving')
tasks = [groceries, work_cafe, study_home]
week_plan = WeekPlan('34 Halcyon Rd, Newton Centre, MA, 02459', tasks)
_, status = week_plan.add_task_to_day(plan[6], 2, tasks[2], 0, 6)
print(status)
print(plan)