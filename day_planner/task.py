""" Task.py
Defines Task class which is one activity a user needs to complete.
"""
from typing import List, Tuple, TypeVar

class Task:
    def __init__(self, pe: int, total_hours: float, location: str = None, fixed_times: List[List[TypeVar]] = None):
        self.pe = pe # perceived energy taken per hour of working on the task, from 1-10 (1 is a very easy task, 10 is a very draining task)
        self.total_hours = total_hours # total number of hours user needs to work on this task in the week (decimal portion must be in quarters)
        self.location = location # address of the task if the task needs to be completed in a certain location
        self.fixed_times = fixed_times # List[List[day: str, start_time: int, end_time:int]] where day is day of the week task needs 
                                       # to be completed and start and end times are times task needs to be comlplted (military time int)
        