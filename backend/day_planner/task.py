""" Task.py
Defines Task class which represents a single task a user needs scheduled.
"""
from typing import List, TypeVar

class Task:
    def __init__(self, name: str, pe: int, total_hours: float, location: str = None, fixed_time: List[List[TypeVar]] = None, mode:str ="walking"):
        self.name = name # description of task
        self.pe = pe # perceived energy taken per hour of working on the task, from 1-10 (1 is a very easy task, 10 is a very draining task)
        self.total_hours = total_hours # total number of hours user needs to work on this task in the week (decimal portion must be in quarters)
        self.location = location # address of the task if the task needs to be completed in a certain location
        self.fixed_time = fixed_time # List[day: str, start_time: float, end_time: float] where day is day of the week task needs 
                                       # to be completed and start and end times are times task needs to be comlplted (military time int),
        self.mode = mode #mode of transportation one of walking, transit, driving, bicycling

        