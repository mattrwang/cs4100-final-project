""" week_plan.py
Defines WeekPlan class which is the plan for a week with scheduled tasks.
"""
from Task import Task
from typing import List, Tuple
# from hill_descent import energy_function
import numpy as np
from get_transport_time import get_transport_time
import math

class WeekPlan:
    def __init__(self, home: str, tasks: List[Task], api_key: str, day_start_time: float=9.0, day_end_time:float=17.0):
        self.home = home # home address that user needs to start from and end up at 
        self.tasks = tasks # list of tasks user needs scheduled
        self.api_key = api_key # api key for Google Maps API
        self.day_start_time = day_start_time # time when planned tasks may begin on each day (military time float, decimal must be factor of 25)
        self.day_end_time = day_end_time # time when planned tasks must end by on each day (military time float, decimal must be factor of 25)
        # self.plan = self.generate_random_plan(self.tasks, self.day_start_time, self.day_end_time)
        # self.total_energy = energy_function(self.plan, self.tasks, self.api_key) # total energy of the week plan
    
    
    def add_task_to_day(self, day_plan: np.array, t_i: int, task: Task, i_start: int, i_end: int) -> Tuple[np.array, int]:
        # day plan: array day plan
        # t_i: index of task to add in self.tasls
        # task: Task to add
        # i_start: start interval of the task
        # i_end: end interval of the task (task scheduled up to this interval, not including)

        # intialize new plan for the day
        new_day_plan = day_plan.copy()
        try:
            # task cannot be added to the day if the task's time interval is occupied by another task
            if np.all(new_day_plan[i_start:i_end]>0):
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
                to_intvs = math.ceil(get_transport_time(start_loc, task.location, task.mode, self.api_key)/5)
                # task cannot be scheduled if another task occupies transportation timeslot
                if np.all(new_day_plan[i_start-to_intvs:i_start]>0):
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
                    from_intvs = math.ceil(get_transport_time(task.location, next_tasks_new_loc[0][1], self.tasks[next_tasks_new_loc[0][0]-1].mode, self.api_key)/5)
                    # set from transportation intervals if no tasks exist during this inverval 
                    if np.all(new_day_plan[next_task_i-from_intvs:next_task_i]<=0):
                        # set all intervals from end of task to beginign of next time to free time
                        new_day_plan[i_end:next_task_i] = 0
                        # add tranportation time from task
                        new_day_plan[next_task_i-from_intvs:next_task_i] = np.array([next_tasks_new_loc[0][0]*-1 for _ in range(from_intvs)])
                    # reschedule task if another task occupies transportation intervals
                    else:
                        raise

                # check there is enough time to get home from this task if there is no task or another task without a location after it
                if len(next_tasks_new_loc)==0:
                    # compute transportation intervals from task to home
                    from_intvs = math.ceil(get_transport_time(task.location, self.home, task.mode, self.api_key)/5)
                    # get intervals after this task, either immidately after if this is last task or after next task without a location
                    after_day_plan = new_day_plan[i_end:] if np.all(new_day_plan[i_end:]==0) else new_day_plan[i_end:][np.nonzero(new_day_plan[i_end:])[0][-1]+1:]
                    # task cannot be scheduled if it requires more time to get home than time that exists
                    if after_day_plan.shape[0]>from_intvs:
                        raise
                # set status as completed           
                status = 1
        except: 
                new_day_plan = day_plan.copy()
                status = 0
        return new_day_plan, status
    

    # def valid_plan(self, plan: np.array) -> bool:
    #     # TODO
    #     return True
    
    # def generate_random_plan(self, tasks: List[Task], day_start_time: float=9.0, day_end_time: float=17.0) -> np.array:
    #     """
    #     Generates a random plan with tasks randomly inserted in different timelots.
    #     Fixed time tasks are correctly put in their given timeslot.

    #     Args:
    #         tasks (List[Task]): tasks the user needs scheduled
    #         day_start_time (float): time when planned tasks may begin on each day (military time float, decimal must be factor of 25)
    #         day_end_time (float): time when planned tasks must emd by on each day (military time float, decimal must be factor of 25)
    #     Returns:
    #         plan (np.array): scheduled activites for the week as a 7xn array, each row is day of the week (ordered Sun, Mon, ...) with 15 minute time intervals for the given day timeperiod 
    #     """ 
    #     # define a dictionary mapping string day to int day
    #     day2int = {'sun': 0, 'mon': 1, 'tue':2, 'wed':3, 'thu':4, 'fri':5, 'sat':6}
    #     # calculate number of 15-minute time intervals for each day
    #     n = int((day_end_time-day_start_time)*12)
    #     # intialize the week plan, each available timeslot is 0
    #     plan = np.zeros((7, n), dtype=int)
    #     # save tasks with fixed days and times
    #     # TODO: order from earlier to later in day
    #     fixed_time_tasks = [(j, t) for j,t in enumerate(tasks) if t.fixed_time[1] is not None]
    #     # same tasks with fixed days but not times
    #     fixed_day_tasks = [(j, t) for j,t in enumerate(tasks) if t.fixed_time is not None and t.fixed_time[1] is None]
    #     # save non-fixed tasks
    #     non_fixed_tasks = [(j, t) for j,t in enumerate(tasks) if t.fixed_time is None]
        
    #     # assign fixed time tasks to their correct day and time 
    #     for (j, task) in fixed_time_tasks:
    #         # integer day of task
    #         day = day2int[task.fixed_time[0]]
    #         # index of interval start of task
    #         i_start = int((task.fixed_time[1]-self.day_start_time)*12)
    #         # index of interval end of task
    #         i_end = int((task.fixed_time[2]-task.fixed_time[1])*12)+i_start
    #         # add task to plan
    #         new_day_plan, status = add_task_to_day(plan[day], j, task, i_start, i_end)
    #         # save new plan for the day
    #         plan[day] = new_day_plan
        
    #     # assign fixed day tasks to their correct day 
    #     for (j, task) in fixed_time_tasks:
    #         # intialize variable if the task needs to be rescheduled
    #         reschedule = True
    #         # keep finding an interval for the task while the current scheduled time for the task is not valid
    #         while reschedule:
    #             # integer day of task
    #             day = day2int[task.fixed_time[0]]
    #             # get random index of start interval
    #             i_start = np.random.randint(0, n)
    #             # compute index of end interval
    #             i_end = int(task.total_hours*12)+i_start
    #             # if the time interval already has a task, reschedule the current task
    #             if not np.array_equiv(plan[day][i_start:i_end], np.zeros(i_end-i_start)):
    #                 break
    #             # schedule task at this interval and add transporation intervals
    #             new_day_plan, status = self.add_task_to_day(plan[day], j, task, i_start, i_end)
    #             if status != 1 or not self.valid_plan(np.array(new_day_plan)):
    #                 reschedule = True
    #             else:
    #                 plan[day] = new_day_plan
    #     """  
    #     # schedule remaining activities in random intervals
    #     for (j, task) in non_fixed_tasks:
    #         # get random day of week
    #         day = np.random.randint(0, 7)
    #         # get random index of start interval
    #         i_start = np.random.randint(0, n)
    #         # compute index of end interval
    #         i_end = int(task.total_hours*12)+i_start
    #         # keep getting random day and start time while there is not enough time to complete task continuously
    #         while not np.array_equal(plan[day][i_start:i_end], np.array([-1 for _ in range(i_end-i_start)])):
    #             day = np.random.randint(0, 7)
    #             i_start = np.random.randint(0, n)
    #             i_end = int(task.total_hours*12)+i_start
    #         plan[day][i_start:i_end] = np.array([j for _ in range(i_end-i_start)])"""
            
    #     return plan
    
