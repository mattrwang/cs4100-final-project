""" week_plan.py
Defines WeekPlan class which is the plan for a week with scheduled tasks.
"""
from Task import Task
from typing import List, Tuple
# from hill_descent import energy_function
import numpy as np
from transport_time import estimate_transport_time
import math

class WeekPlan:
    def __init__(self, home: str, tasks: List[Task], api_key: str=None, day_start_time: float=9.0, day_end_time:float=19.0):
        self.home = home # home address that user needs to start from and end up at 
        self.tasks = tasks # list of tasks user needs scheduled
        self.api_key = api_key # api key for Google Maps API
        self.day_start_time = day_start_time # time when planned tasks may begin on each day (military time float, decimal must be factor of 25)
        self.day_end_time = day_end_time # time when planned tasks must end by on each day (military time float, decimal must be factor of 25)
        self.plan = None # intialize plan for the week
        self.total_energy = -1 # intialize total energy of the week plan
        self.fixed_time_tasks = [i+1 for i, task in enumerate(tasks) if task.fixed_time is not None and task.fixed_time[1] is not None] 
    

    def add_task_to_day(self, day_plan: np.array, t_i: int, task: Task, i_start: int, i_end: int) -> Tuple[np.array, int]:
        """
        Adds a task to a day plan if there are no conflicts with existing tasks in the plan.
        Adds in transportation time denoted as the negative task index. Transportation from home to first task is scheduled.
        Trasnportation from the last task to home is ensured to be possible, but not scheduled.

        Args:
            day_plan (npp.array): plan for the day
            t_i (int): index of the task 
            i_start (int): index of start interval of the task
            i_end (int):index of the end interval of the task (task scheduled up to, not including this interval)
        Returns:
            new_day_plan (np.array): new day plan (with the task if it's possible to schedule it)
            status (int): status of if the task was able to be scheduled
        """ 
        # intialize new plan for the day
        new_day_plan = day_plan.copy()
        # intialize status as complete
        status = 1
        try:
            # task cannot be added to the day if the task's time interval is occupied by another task
            if np.any(new_day_plan[i_start:i_end]>0):
                raise
            # assign task to it's given time interval
            new_day_plan[i_start:i_end] = np.array([t_i+1 for _ in range(i_end-i_start)])
            if task.location is not None:
                # compute transportation time from previous location to current task location
                # get previous tasks
                prev_tasks = [i for i in new_day_plan[0:i_start] if i!=0]
                # get location of task that comes right before this task (if this is the first task of the day then previous location is home)
                start_loc = self.home if len(prev_tasks) == 0 else self.tasks[prev_tasks[-1]-1].location
                # get number of intervals it will take to get to location of this task
                to_intvs = math.ceil(estimate_transport_time(start_loc, task.location, task.mode)/5)
                # task cannot be scheduled if another task occupies transportation timeslot
                if np.any(new_day_plan[i_start-to_intvs:i_start]>0):
                    raise
                # add transportation intervals to day plan
                new_day_plan[i_start-to_intvs:i_start] = np.array([(t_i+1) for _ in range(to_intvs)])*-1 
                # update transportation time for first task following this task with a new location
                # get tasks that come after this task
                next_tasks = [(t_i, self.tasks[t_i-1].location, i+i_end) for i, t_i in enumerate(new_day_plan[i_end:]) if t_i>0]
                # get task index, location, and day interval index for next tasks in a new location
                next_tasks_new_loc = [(t_i, loc, i) for t_i, loc, i in next_tasks if t_i!=0 and loc not in [None, task.location]]
                if len(next_tasks_new_loc)>0:
                    next_task_i = next_tasks_new_loc[0][2]
                    from_intvs = math.ceil(estimate_transport_time(task.location, next_tasks_new_loc[0][1], self.tasks[next_tasks_new_loc[0][0]-1].mode)/5)
                    # set from transportation intervals if no tasks exist during this inverval 
                    if np.all(new_day_plan[next_task_i-from_intvs:next_task_i]<=0):
                        # set all intervals from end of task to beginign of next time to free time
                        new_day_plan[i_end:next_task_i] = 0
                        # add tranportation time from task
                        new_day_plan[next_task_i-from_intvs:next_task_i] = np.array([next_tasks_new_loc[0][0]*-1 for _ in range(from_intvs)])
                    # reschedule task if another task occupies transportation intervals
                    else:
                        raise

                # schedule trasportation from this task to home if there is no other task or no task with a new location after added task
                if len(next_tasks_new_loc)==0:
                    # get rest of the day after added task
                    rest_day_plan = new_day_plan[i_end:] 
                    # get index of rest of day, either right after this task or last task if there are more tasks after this
                    i_rest = i_end if np.all(new_day_plan[i_end:]<=0) else i_end+np.argmax(rest_day_plan != 0)
                    # get index to set for transportation to home
                    i_get_home = -1*(t_i+1) if i_rest==i_end else abs(rest_day_plan[np.nonzero(rest_day_plan)[0][-1]])*-1
                    # compute transportation intervals from task to home
                    from_intvs = math.ceil(estimate_transport_time(task.location, self.home, task.mode)/5)
                    # task cannot be scheduled if it requires more time to get home than time that exists
                    if new_day_plan[i_rest:].shape[0]<from_intvs:
                        raise
                    rest_day_plan = new_day_plan[i_end:]
                    rest_day_plan[rest_day_plan.shape[0]-from_intvs:] = i_get_home
                    new_day_plan[i_end:] = rest_day_plan
        except: 
            new_day_plan = day_plan.copy()
            status = 0
        return new_day_plan, status
    
    def generate_random_plan(self, tasks: List[Task], day_start_time: float=9.0, day_end_time: float=19.0) -> np.array:
        """
        Generates a random plan with tasks randomly inserted in different timelots.
        Fixed time tasks are correctly put in their given timeslot.

        Args:
            tasks (List[Task]): tasks the user needs scheduled
            day_start_time (float): time when planned tasks may begin on each day (military time float, decimal must be factor of 25)
            day_end_time (float): time when planned tasks must emd by on each day (military time float, decimal must be factor of 25)
        Returns:
            plan (np.array): scheduled activites for the week as a 7xn array, each row is day of the week (ordered Sun, Mon, ...) with 15 minute time intervals for the given day timeperiod 
        """ 
        # define a dictionary mapping string day to int day
        day2int = {'Sunday': 0, 'Monday': 1, 'Tuesday':2, 'Wednesday':3, 'Thursday':4, 'Friday':5, 'Saturday':6}
        # calculate number of 5-minute time intervals for each day
        n = int((day_end_time-day_start_time)*12)
        # intialize the week plan, each available timeslot is 0
        plan = np.zeros((7, n), dtype=int)
        # save tasks with fixed days and times
        fixed_time_tasks = [(j, t) for j,t in enumerate(tasks) if t.fixed_time is not None and t.fixed_time[1] is not None]
        # save tasks with fixed days but not times
        fixed_day_tasks = [(j, t) for j,t in enumerate(tasks) if t.fixed_time is not None and t.fixed_time[1] is None]
        # save non-fixed tasks
        non_fixed_tasks = [(j, t) for j,t in enumerate(tasks) if t.fixed_time is None]
        
        # assign fixed time tasks to their correct day and time 
        for (j, task) in fixed_time_tasks:
            # integer day of task
            day = day2int[task.fixed_time[0]]
            # index of interval start of task
            i_start = int(round((task.fixed_time[1]-self.day_start_time)*12, 1))
            # index of interval end of task
            i_end = int((task.fixed_time[2]-task.fixed_time[1])*12)+i_start
            # add task to plan
            new_day_plan, status = self.add_task_to_day(plan[day], j, task, i_start, i_end)
            # save new plan for the day
            plan[day] = new_day_plan
        print('fixed day time tasks assigned')
        
        # assign fixed day tasks to their correct day and a random tipe
        for (j, task) in fixed_day_tasks:
            # intialize variable if the task needs to be rescheduled
            reschedule = True
            # keep finding an interval for the task while the current scheduled time for the task is not valid
            while reschedule:
                # integer day of task
                day = day2int[task.fixed_time[0]]
                # get random index of start interval
                i_start = np.random.randint(0, n)
                # compute index of end interval
                i_end = int(round(task.total_hours*12, 1))+i_start
                # schedule task at this interval
                new_day_plan, status = self.add_task_to_day(plan[day], j, task, i_start, i_end)
                if status == 1:
                    reschedule = False
                    plan[day] = new_day_plan
        print('fixed day tasks assigned')

        # schedule remaining activities in random intervals
        for (j, task) in non_fixed_tasks:
            reschedule = True
            while reschedule:
                print(f"Task {task.name} resheduled")
                # get random day of week
                day = np.random.randint(0, 7)
                # get random index of start interval
                i_start = np.random.randint(0, n)
                # compute index of end interval
                i_end = int(round(task.total_hours*12,1))+i_start
                # add task to the day
                new_day_plan, status = self.add_task_to_day(plan[day], j, task, i_start, i_end)
                if status == 1:
                    reschedule = False
                    plan[day] = new_day_plan
        print('non fixed tasks assigned')
        return plan
    
    def valid_plan(self, plan: np.array) -> bool:
        day2int = {'Sunday': 0, 'Monday': 1, 'Tuesday':2, 'Wednesday':3, 'Thursday':4, 'Friday':5, 'Saturday':6}
        # checks each task is in the plan for the correct amount of time
        for i, task in enumerate(self.tasks):
            if not np.count_nonzero(plan == i+1) == round(task.total_hours*12, 1):
                return False
        
        # check that fixed day and time tasks are in correct position
        fixed_time_tasks = [(j, t) for j,t in enumerate(self.tasks) if t.fixed_time is not None and t.fixed_time[1] is not None]
        for t in fixed_time_tasks:
            j = t[0]
            task = t[1]
            i_start = int(round((task.fixed_time[1]-self.day_start_time)*12, 1))
            i_end = int((task.fixed_time[2]-task.fixed_time[1])*12)+i_start
            plan[day2int[task.fixed_time[0]]][i_start:i_end] = np.ones(i_end-i_start)*(j)
        # save tasks with fixed days but not times
        fixed_day_tasks = [(j, t) for j,t in enumerate(self.tasks) if t.fixed_time is not None and t.fixed_time[1] is None]
        for t in fixed_day_tasks:
            j = t[0]
            task = t[1]
            if not np.count_nonzero(plan[day2int[task.fixed_time[0]]] == j+1) == round(task.total_hours*12, 1):
                return False
        return True
    
