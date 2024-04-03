from FILE_READER import read_files
from DATE_PARSER import tabulate_days
import pandas as pd
import numpy as np
from datetime import datetime

lines_2021 = read_files("backend/snell_density/Snell Data/2021")
table_2021 = tabulate_days(lines_2021)
reshaped_table_2021 = table_2021.reshape(-1, 1)

lines_2022 = read_files("backend/snell_density/Snell Data/2022")
table_2022 = tabulate_days(lines_2022)
reshaped_table_2022 = table_2022.reshape(-1, 1)

reshaped_table = np.concatenate((reshaped_table_2021, reshaped_table_2022))

start_date = "2021-01-01 00:00:00"
end_date = "2022-12-31 23:00:00"

date_range = pd.date_range(start=start_date, end=end_date, freq='h')

df = pd.DataFrame(reshaped_table, columns=['count'])
df['datetime'] = date_range[:len(reshaped_table)]
df['year_after_2021'] = df['datetime'].apply(lambda x: x.year - 2021)
df['month'] = df['datetime'].apply(lambda x: x.month)
df['day'] = df['datetime'].apply(lambda x: x.day)
df['hour'] = df['datetime'].apply(lambda x: x.hour)
df['day_of_week'] = df['datetime'].apply(lambda x: x.weekday())

df = df[['month', 'day', 'year_after_2021', 'hour', 'day_of_week', 'count']]

df.to_csv("backend/snell_density/data.csv", index=False)

# print(len(lines), " items") #1579308
# print(table)
# print(sum(table[2])) # expect 436 entries on january 3rd