import re
import numpy as np

# Takes list of dates, elements formatted as "YYYY-MM-DD HH:MM:SS",
# and returns a numpy array tabulating # of occurerences for 
# each hour for every day
def tabulate_days(l):
    regex = r"\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2}"
    table = np.zeros((365, 24))
    for date in l:
        hour = int(date[11:13])
        if re.match(regex, date) and 0 <= hour <= 23: # check hour
            index = day_number(date[5:10]) # checks month & day
            if index >= 0:
                table[index][hour] += 1
        else:
            print(f"Argument: {date} is not well formed. Skipping")
    return table



# Takes in string formatted as "MM-DD" and returns the number of days
# since January 1, assumes 365 days, non leap year. -1 if not well formed
def day_number(str):
    regex = r"\d{2}\-\d{2}"
    if re.match(regex, str):
        month_to_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        month = int(str[:2])-1
        day = int(str[3:])
        if 0 <= month <= 12 and 1 <= day <= month_to_day[month]:
            return sum(month_to_day[:month]) + day - 1 # january 1 = 0
    return -1

# testing
#l = ['2022-01-09 08:54:37', '2022-01-09 12:01:19', '2022-01-09 12:07:07', '2022-01-09 14:36:06', '2022-01-09 15:44:42']
#table = tabulate_days(l)
#print(table[8])

    
    
