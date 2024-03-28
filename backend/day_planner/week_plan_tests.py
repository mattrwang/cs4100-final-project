from WeekPlan import WeekPlan
from Task import Task
import numpy as np

API_KEY = ''

def test_add_task_to_day():
     # case 1: adding a task between two tasks that requires changing transportation time before and after task
    day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                        1,1,1,1,1,1,0,0,0,0,0,0, 
                        0,0,0,0,0,0,0,0,0,0,0,0,
                        2,2,2,2,2,2,2,2,2,2,2,2])
    home = '34 Halcyon Rd, Newton Centre, MA, 02459'
    groceries = Task(3, 0.5, '647 Washington St, Newton, MA, 02458', ['sun', 10.0, 10.5], 'driving')
    work_cafe = Task(4, 1.0, '1334 Boylston Street, Boston, MA 02215', ['sun', 12.0, 13.0], 'driving')
    walk_park = Task(2, 0.416666, '1094 Beacon St, Newton, MA 02461', None, 'driving')
    tasks = [groceries, work_cafe, walk_park]  
    week_plan = WeekPlan(home, tasks, API_KEY)
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 2, walk_park, 25, 30)
    actual_new_day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                        1,1,1,1,1,1,0,0,0,0,0,-3, 
                        -3,3,3,3,3,3,0,0,-2,-2,-2,-2,
                        2,2,2,2,2,2,2,2,2,2,2,2])
    assert status == 1
    assert np.array_equiv(new_day_plan, actual_new_day_plan)

    # case 2: adding a task as the first/last task of the day before heading home in a location that is not home
    # first
    day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,2,2,2,2,2,2,2,2,2,2])
    actual_new_day_plan = np.array([-3,3,3,3,3,3,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,2,2,2,2,2,2,2,2,2,2])
    assert status == 1
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 2, walk_park, 1, 6)
    assert np.array_equiv(new_day_plan, actual_new_day_plan)
   
    
    # last
    day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,0,0,0,0,0,0,0,0,0,0])
    groceries = Task(3, 0.5, '647 Washington St, Newton, MA, 02458', ['sun', 10.0, 10.5], 'driving')
    work_cafe = Task(4, 0.166666, '1334 Boylston Street, Boston, MA 02215', ['sun', 12.0, 12.166666], 'driving')
    walk_park = Task(4, 0.33333, '1109 Beacon St, Newton, MA, 02459', None,'driving')

    tasks = [groceries, work_cafe, walk_park]
    actual_new_day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,0,-3,-3,-3,-3,3,3,3,3,-3])
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 2, walk_park, 43, 47)
    assert status == 1
    assert np.array_equiv(new_day_plan, actual_new_day_plan)

    # case 3: adding a task that requires overwriting another task's alloted time (fail)
    day_plan = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    groceries = Task(3, 1.0, None, ['sun', 9.0, 10.0], 'driving')
    walk_park = Task(4, 1.0, None, ['sun', 9.0, 10.0],'driving')
    tasks = [groceries, walk_park]
    actual_new_day_plan = day_plan
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 1, walk_park, 43, 47)
    assert status == 0
    assert np.array_equiv(new_day_plan, actual_new_day_plan)
test_add_task_to_day()

def test_generate_random_plan():
    home = '34 Halcyon Rd, Newton Centre, MA, 02459'
    groceries = Task(3, 0.5, '647 Washington St, Newton, MA, 02458', ['sun', 10.0, 10.5], 'driving')
    work_cafe = Task(4, 1.0, '1334 Boylston Street, Boston, MA 02215', ['sun', None, None], 'driving')
    study_home = Task(2, 0.416666, home, None, 'driving')
    tasks = [groceries, work_cafe, study_home]

    week_plan = WeekPlan(home, tasks, API_KEY)
    plan = week_plan.generate_random_plan(tasks)
    # check each task is in th eplan for the specified time intervals
    assert np.count_nonzero(plan == 1) == 6
    assert np.count_nonzero(plan == 2) == 12
    assert np.count_nonzero(plan == 3) == 5

test_generate_random_plan()

def test_valid_plan():
    # case 1: valid plan
    home = '34 Halcyon Rd, Newton Centre, MA, 02459'
    groceries = Task(3, 0.5, '647 Washington St, Newton, MA, 02458', ['sun', 10.0, 10.5], 'driving')
    work_cafe = Task(4, 1.0, '1334 Boylston Street, Boston, MA 02215', ['sun', None, None], 'driving')
    study_home = Task(2, 0.5, home, None, 'driving')
    tasks = [groceries, work_cafe, study_home]

    week_plan = WeekPlan(home, tasks, API_KEY)
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
    assert week_plan.valid_plan(plan)
    
    # case 2: missing one interval for task 3 (not valid)
    week_plan = WeekPlan(home, tasks, API_KEY)
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
    assert not week_plan.valid_plan(plan)
test_valid_plan()
