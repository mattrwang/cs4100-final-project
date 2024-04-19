from task import Task
import csv
import math


def input_parser(d):
    with open(d, "r") as file:
        reader = csv.reader(file)
        next(reader)
        tasks = []
        for line in reader:
            duration = line[3]
            hours = int(duration[:2])
            min = int(duration[3:])
            decimal = (int(math.ceil(min / 5.0)) * 5)/60
            if line[2] != "":
                location = str(line[2])
                if line[4] != "":
                    if line[5] != "":
                        start_hour = int(line[5][:2])
                        start_min = int(line[5][3:])
                        start_decimal = (int(math.ceil(start_min / 5.0)) * 5)/60
                        end_hour = int(line[6][:2])
                        end_min = int(line[6][3:5])
                        end_decimal = (int(math.ceil(end_min / 5.0)) * 5)/60
                        fixed_time = [line[4], start_hour+start_decimal, end_hour+end_decimal]
                    else:
                        fixed_time = [line[4], None, None]
                    task = Task(line[0], int(line[1]), hours + decimal, line[2], fixed_time)
                task = Task(line[0], int(line[1]), hours + decimal, line[2])
            task = Task(line[0], int(line[1]), hours + decimal, location=location)
            tasks.append(task)
    return tasks
