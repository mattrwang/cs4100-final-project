""" WeekPlan.py
Defines WeekPlan class which is the plan for a week with scheduled tasks.
"""
from task import Task
from typing import List
from hill_descent import energyfunction
import numpy as np

class WeekPlan:
    def __init__(self, tasks: List[Task], day_start_time: float=9.0, day_end_time:float=17.0):
        self.tasks = tasks # list of tasks user needs scheduled
        self.day_start_time = day_start_time # time when planned tasks may begin on each day (military time float, decimal must be factor of 25)
        self.day_end_time = day_end_time # time when planned tasks must end by on each day (military time float, decimal must be factor of 25)
        self.plan = self.generate_random_plan(self.tasks, self.day_start_time, self.day_end_time)
        self.total_energy = energyfunction(self.plan, self.tasks) # total energy of the week plan
    
    def generate_random_plan(self, tasks: List[Task], day_start_time: float=9.0, day_end_time: float=17.0) -> np.array:
        """
        Generates a random plan with tasks randomly inserted in different timelots.
        Fixed time tasks are correctly put in their given timeslot.

        Args:
            tasks (List[Task]): tasks the user needs scheduled
            day_start_time (float): time when planned tasks may begin on each day (military time float, decimal must be factor of 25)
            day_end_time (float): time when planned tasks must emd by on each day (military time float, decimal must be factor of 25)
        Returns:
            week_plan (np.array): scheduled activites for the week as a 7xn array, each row is day of the week (ordered Sun, Mon, ...) with 15 minute time intervals for the given day timeperiod 
        """ 
        # define a dictionary mapping string day to int day
        day2int = {'sun': 0, 'mon': 1, 'tue':2, 'wed':3, 'thu':4, 'fri':5, 'sat':6}
        # calculate number of 15-minute time intervals for each day
        n = int((day_end_time-day_start_time)*4)
        # intialize the week plan, each timeslot starts as -1
        plan = np.ones((7, n))*-1
        # save fixed tasks
        fixed_tasks = [(j, t) for j,t in enumerate(tasks) if t.fixed_times is not None]
        # save non-fixed tasks
        non_fixed_tasks = [(j, t) for j,t in enumerate(tasks) if t.fixed_times is None]
        
        # assign fixed tasks to their correct time slot
        for (j, task) in fixed_tasks:
            for times in task.fixed_times:
                # integer day of task
                day = day2int[times[0]]
                # index of interval start of task
                i_start = int((times[1]-self.day_start_time)*4)
                # index of interval end of task
                i_end = int((times[2]-times[1])*4)+i_start
                plan[day][i_start:i_end] = np.array([j for _ in range(i_end-i_start)])
        
        # schedule remaining activities in random intervals
        for (j, task) in non_fixed_tasks:
            # get random day of week
            day = np.random.randint(0, 7)
            # get random start interval
            i_start = np.random.randint(0, n)
            # compute random end interval
            i_end = int(task.total_hours*4)+i_start
            # keep getting random day and start time while there is not enough time to complete task continuously
            while not np.array_equal(plan[day][i_start:i_end], np.array([-1 for _ in range(i_end-i_start)])):
                day = np.random.randint(0, 7)
                i_start = np.random.randint(0, n)
                i_end = int(task.total_hours*4)+i_start
            plan[day][i_start:i_end] = np.array([j for _ in range(i_end-i_start)])
            
        return plan
