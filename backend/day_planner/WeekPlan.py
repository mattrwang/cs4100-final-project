""" week_plan.py
Defines WeekPlan class which is the plan for a week with scheduled tasks.
"""
from task import Task
from typing import List, Tuple
import numpy as np
from transport_time import estimate_transport_time
import math
import threading      
import random

class WeekPlan:
    def __init__(self, home: str, tasks: List[Task], api_key: str=None, day_start_time: float=9.0, day_end_time:float=21.0):
        self.home = home # home address that user needs to start from and end up at 
        self.tasks = tasks # list of tasks user needs scheduled
        self.api_key = api_key # api key for Google Maps API
        self.day_start_time = day_start_time # time when planned tasks may begin on each day (military time float, decimal must be factor of 25)
        self.day_end_time = day_end_time # time when planned tasks must end by on each day (military time float, decimal must be factor of 25)
        self.plan = None # intialize plan for the week
        self.total_energy = -1 # intialize total energy of the week plan
        self.fixed_time_tasks = [i+1 for i, task in enumerate(tasks) if task.fixed_time is not None and task.fixed_time[1] is not None] 
        self.day2int = {'Sunday': 0, 'Monday': 1, 'Tuesday':2, 'Wednesday':3, 'Thursday':4, 'Friday':5, 'Saturday':6}        

    

    def add_task_to_day(self, day_plan: np.array, t_i: int, task: Task, i_start: int, i_end: int) -> Tuple[np.array, int]:
        """
        Adds a task to a day plan if there are no conflicts with existing tasks in the plan.
        Adds in transportation time denoted as the negative task index. Transportation from home to first task is scheduled.
        Transportation from the last task to home is ensured to be possible, but not scheduled.

        Args:
            day_plan: plan for the day
            t_i: index of the task 
            i_start: index of start interval of the task
            i_end:index of the end interval of the task (task scheduled up to, not including this interval)
        Returns:
            new_day_plan: new day plan (with the task if it's possible to schedule it)
            status: status of if the task was able to be scheduled
        """ 
        # Initialize new plan for the day
        new_day_plan = day_plan.copy()
        # Initialize status as complete
        status = 1
        
        try:
            # Check if the task's time interval is occupied by another task
            if np.any(new_day_plan[i_start:i_end] > 0):
                raise ValueError("Task time interval is occupied")
            
            # Assign the task to its given time interval
            new_day_plan[i_start:i_end] = np.array([t_i+1 for _ in range(i_end - i_start)])
            
            # Add transportation time if the task has a location
            if task.location is not None:
                # Compute transportation time from previous location to current task location
                prev_tasks = [i for i in new_day_plan[0:i_start] if i != 0]
                start_loc = self.home if len(prev_tasks) == 0 else self.tasks[prev_tasks[-1] - 1].location
                to_intvs = math.ceil(estimate_transport_time(start_loc, task.location, task.mode) / 5)
                if np.any(new_day_plan[i_start - to_intvs:i_start] > 0):
                    raise ValueError("Transportation timeslot is occupied")
                new_day_plan[i_start - to_intvs:i_start] = np.array([(t_i + 1) for _ in range(to_intvs)]) * -1 
                
                # Update transportation time for the first task following this task with a new location
                next_tasks = [(t_i, self.tasks[t_i - 1].location, i + i_end) for i, t_i in enumerate(new_day_plan[i_end:]) if t_i > 0]
                next_tasks_new_loc = [(t_i, loc, i) for t_i, loc, i in next_tasks if t_i != 0 and loc not in [None, task.location]]
                if len(next_tasks_new_loc) > 0:
                    next_task_i = next_tasks_new_loc[0][2]
                    from_intvs = math.ceil(estimate_transport_time(task.location, next_tasks_new_loc[0][1], self.tasks[next_tasks_new_loc[0][0] - 1].mode) / 5)
                    if np.all(new_day_plan[next_task_i - from_intvs:next_task_i] <= 0):
                        new_day_plan[i_end:next_task_i] = 0
                        new_day_plan[next_task_i - from_intvs:next_task_i] = np.array([next_tasks_new_loc[0][0] * -1 for _ in range(from_intvs)])
                    else:
                        raise ValueError("Transportation timeslot is occupied")
                
                # Schedule transportation from this task to home
                if len(next_tasks_new_loc) == 0:
                    rest_day_plan = new_day_plan[i_end:]
                    i_rest = i_end if np.all(new_day_plan[i_end:] <= 0) else i_end + np.argmax(rest_day_plan != 0)
                    i_get_home = -1 * (t_i + 1) if i_rest == i_end else abs(rest_day_plan[np.nonzero(rest_day_plan)[0][-1]]) * -1
                    from_intvs = math.ceil(estimate_transport_time(task.location, self.home, task.mode) / 5)
                    if new_day_plan[i_rest:].shape[0] < from_intvs:
                        raise ValueError("Not enough time to get home")
                    rest_day_plan[rest_day_plan.shape[0] - from_intvs:] = i_get_home
                    new_day_plan[i_end:] = rest_day_plan
                    
        except ValueError as e:
            new_day_plan = day_plan.copy()
            status = 0
        
        return new_day_plan, status
    
    def generate_random_plan_with_timeout(self, tasks: List[Task], timeout_sec=5) -> np.array:
        """
        Generates a random plan but times out and re-starts generation if a plan has not been generated in
         the specified amount fo seconds. 

        Args:
            tasks: tasks the user needs scheduled
            timeout_sec: number of seconds to wait for plan to generate before generating a different plan
        Returns:
            plan: scheduled activites for the week as a 7xn array, each row is day of the week (ordered Sun, Mon, ...) with 15 minute time intervals for the given day timeperiod 
        """ 
        result = []

        def target():
            result.append(self.generate_random_plan(tasks))

        thread = threading.Thread(target=target)
        thread.start()
        thread.join(timeout_sec)

        if thread.is_alive():
            thread.join()  

        if result:  
            return result[0]  
        else:
            return None  

    def generate_random_plan(self, tasks: List[Task]) -> np.array:
        """
        Generates a random plan with tasks randomly inserted in different timelots.
        Fixed time tasks are correctly put in their given timeslot.

        Args:
            tasks: tasks the user needs scheduled
        Returns:
            plan (np.array): scheduled activites for the week as a 7xn array, each row is day of the week (ordered Sun, Mon, ...) with 15 minute time intervals for the given day timeperiod 
        """ 
        # calculate number of 5-minute time intervals for each day
        n = int((self.day_end_time-self.day_start_time)*12)
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
            day = self.day2int[task.fixed_time[0]]
            # index of interval start of task
            i_start = int(round((task.fixed_time[1]-self.day_start_time)*12, 1))
            # index of interval end of task
            i_end = int((task.fixed_time[2]-task.fixed_time[1])*12)+i_start
            # add task to plan
            new_day_plan, status = self.add_task_to_day(plan[day], j, task, i_start, i_end)
            # save new plan for the day
            plan[day] = new_day_plan
        
        # assign fixed day tasks to their correct day and a random tipe
        for (j, task) in fixed_day_tasks:
            # intialize variable if the task needs to be rescheduled
            reschedule = True
            # keep finding an interval for the task while the current scheduled time for the task is not valid
            while reschedule:
                # integer day of task
                day = self.day2int[task.fixed_time[0]]
                # get random index of start interval
                i_start = random.randint(0, n)
                # compute index of end interval
                i_end = int(round(task.total_hours*12, 1))+i_start
                # schedule task at this interval
                new_day_plan, status = self.add_task_to_day(plan[day], j, task, i_start, i_end)
                if status == 1:
                    reschedule = False
                    plan[day] = new_day_plan

        # schedule remaining activities in random intervals
        for (j, task) in non_fixed_tasks:
            reschedule = True
            while reschedule:
                # get random day of week
                day = random.randint(0, 6)
                # get random index of start interval
                i_start = random.randint(0, n)
                # compute index of end interval
                i_end = int(round(task.total_hours*12,1))+i_start
                # add task to the day
                new_day_plan, status = self.add_task_to_day(plan[day], j, task, i_start, i_end)
                if status == 1:
                    reschedule = False
                    plan[day] = new_day_plan
        return plan
    
    def valid_day_tasks(self, plan: np.array) -> bool:
        # check fixed day tasks are in their correct day
        fixed_day_tasks = [(j, t) for j,t in enumerate(self.tasks) if t.fixed_time is not None and t.fixed_time[1] is None]
        for t in fixed_day_tasks:
            j = t[0]
            task = t[1]
            if not np.count_nonzero(plan[self.day2int[task.fixed_time[0]]] == j+1) == round(task.total_hours*12, 1):
                return False
        return True