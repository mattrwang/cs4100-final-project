from WeekPlan import WeekPlan
from Task import Task
import numpy as np


def test_add_task_to_day():
    day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                        1,1,1,1,1,1,0,0,0,0,0,0, 
                        0,0,0,0,0,0,0,0,0,0,0,0,
                        2,2,2,2,2,2,2,2,2,2,2,2])
    
    home = '34 Halcyon Rd, Newton Centre, MA, 02459'
    groceries = Task(3, 0.5, '647 Washington St, Newton, MA, 02458', ['sun', 10.0, 10.5], 'driving')
    work_cafe = Task(4, 1.0, '1334 Boylston Street, Boston, MA 02215', ['sun', 12.0, 13.0], 'driving')
    study_home = Task(2, 0.416666, home, None, 'driving')
    tasks = [groceries, work_cafe, study_home]

    api_key = 'AIzaSyAznW9Pu7RNiFKtvcBBF8V4qukuD0QywZA'

    week_plan = WeekPlan(home, tasks, api_key)

    # case 1: adding a task between two tasks that requires changing transportation time before and after task
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 2, study_home, 25, 30) 
    walk_park = Task(2, 0.416666, '1094 Beacon St, Newton, MA 02461', None, 'driving')
    tasks = [groceries, work_cafe, walk_park]
    actual_new_day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                        1,1,1,1,1,1,0,0,0,-3,-3,-3, 
                        -3,3,3,3,3,3,0,-2,-2,-2,-2,-2,
                        2,2,2,2,2,2,2,2,2,2,2,2])
    assert np.array_equiv(new_day_plan, actual_new_day_plan)
    assert status == 1

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
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 2, walk_park, 1, 6)
    assert np.array_equiv(new_day_plan, actual_new_day_plan)
    assert status == 1
    
    # last
    day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,0,0,0,0,0,0,0,0,0,0])

    work_cafe = Task(4, 0.166666, '1334 Boylston Street, Boston, MA 02215', ['sun', 12.0, 12.166666], 'driving')
    walk_park = Task(4, 0.33333, '1109 Beacon St, Newton, MA, 02459', None,'driving')

    tasks = [groceries, work_cafe, walk_park]
    actual_new_day_plan = np.array([0,0,0,0,0,0,0,0,0,0,-1,-1, 
                         1,1,1,1,1,1,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,0,-2,-2,-2,
                         2,2,-3,-3,-3,-3,-3,3,3,3,3,-3])
    new_day_plan, status = week_plan.add_task_to_day(day_plan, 2, walk_park, 43, 47)
    print(new_day_plan)
    print(new_day_plan-actual_new_day_plan)
    assert status == 1
    assert np.array_equiv(new_day_plan, actual_new_day_plan)
    assert status == 1

    # case 3: adding a task that requires overwriting another task's alloted time (fail)
test_add_task_to_day()