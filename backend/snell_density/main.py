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

breaks = [
    pd.Timestamp('2021-01-01'),
    pd.Timestamp('2021-01-02'),
    pd.Timestamp('2021-01-03'),
    pd.Timestamp('2021-01-04'),
    pd.Timestamp('2021-01-05'),
    pd.Timestamp('2021-01-06'),
    pd.Timestamp('2021-01-07'),
    pd.Timestamp('2021-01-08'),
    pd.Timestamp('2021-01-09'),
    pd.Timestamp('2021-01-10'),
    pd.Timestamp('2021-01-11'),
    pd.Timestamp('2021-01-12'),
    pd.Timestamp('2021-01-13'),
    pd.Timestamp('2021-01-14'),
    pd.Timestamp('2021-01-15'),
    pd.Timestamp('2021-01-16'),
    pd.Timestamp('2021-01-17'),
    pd.Timestamp('2021-01-18'),
    pd.Timestamp('2021-02-15'),
    pd.Timestamp('2021-03-24'),
    pd.Timestamp('2021-04-12'),
    pd.Timestamp('2021-05-31'),
    pd.Timestamp('2021-06-18'),
    pd.Timestamp('2021-07-04'),
    pd.Timestamp('2021-07-05'),
    pd.Timestamp('2021-09-06'),
    pd.Timestamp('2021-10-11'),
    pd.Timestamp('2021-11-11'),
    pd.Timestamp('2021-11-24'),
    pd.Timestamp('2021-11-25'),
    pd.Timestamp('2021-11-26'),
    pd.Timestamp('2021-11-27'),
    pd.Timestamp('2021-11-28'),
    pd.Timestamp('2021-12-20'),
    pd.Timestamp('2021-12-21'),
    pd.Timestamp('2021-12-22'),
    pd.Timestamp('2021-12-23'),
    pd.Timestamp('2021-12-24'),
    pd.Timestamp('2021-12-25'),
    pd.Timestamp('2021-12-26'),
    pd.Timestamp('2021-12-27'),
    pd.Timestamp('2021-12-28'),
    pd.Timestamp('2021-12-29'),
    pd.Timestamp('2021-12-30'),
    pd.Timestamp('2021-12-31'),
    pd.Timestamp('2022-01-01'),
    pd.Timestamp('2022-01-02'),
    pd.Timestamp('2022-01-03'),
    pd.Timestamp('2022-01-04'),
    pd.Timestamp('2022-01-05'),
    pd.Timestamp('2022-01-06'),
    pd.Timestamp('2022-01-07'),
    pd.Timestamp('2022-01-08'),
    pd.Timestamp('2022-01-09'),
    pd.Timestamp('2022-01-10'),
    pd.Timestamp('2022-01-11'),
    pd.Timestamp('2022-01-12'),
    pd.Timestamp('2022-01-13'),
    pd.Timestamp('2022-01-14'),
    pd.Timestamp('2022-01-15'),
    pd.Timestamp('2022-01-16'),
    pd.Timestamp('2022-01-17'),
    pd.Timestamp('2022-02-21'),
    pd.Timestamp('2022-03-14'),
    pd.Timestamp('2022-03-15'),
    pd.Timestamp('2022-03-16'),
    pd.Timestamp('2022-03-17'),
    pd.Timestamp('2022-03-18'),
    pd.Timestamp('2022-03-19'),
    pd.Timestamp('2022-03-20'),
    pd.Timestamp('2022-04-18'),
    pd.Timestamp('2022-05-30'),
    pd.Timestamp('2022-06-20'),
    pd.Timestamp('2022-07-04'),
    pd.Timestamp('2022-09-05'),
    pd.Timestamp('2022-10-10'),
    pd.Timestamp('2022-11-11'),
    pd.Timestamp('2022-11-23'),
    pd.Timestamp('2022-11-24'),
    pd.Timestamp('2022-11-25'),
    pd.Timestamp('2022-11-26'),
    pd.Timestamp('2022-11-27'),
    pd.Timestamp('2022-12-19'),
    pd.Timestamp('2022-12-20'),
    pd.Timestamp('2022-12-21'),
    pd.Timestamp('2022-12-22'),
    pd.Timestamp('2022-12-23'),
    pd.Timestamp('2022-12-24'),
    pd.Timestamp('2022-12-25'),
    pd.Timestamp('2022-12-26'),
    pd.Timestamp('2022-12-27'),
    pd.Timestamp('2022-12-28'),
    pd.Timestamp('2022-12-29'),
    pd.Timestamp('2022-12-30'),
    pd.Timestamp('2022-12-31')
]

date_range = pd.date_range(start=start_date, end=end_date, freq='h')

df = pd.DataFrame(reshaped_table, columns=['count'])
df['datetime'] = date_range[:len(reshaped_table)]
df['year_after_2021'] = df['datetime'].apply(lambda x: x.year - 2021)
df['month'] = df['datetime'].apply(lambda x: x.month)
df['day'] = df['datetime'].apply(lambda x: x.day)
df['hour'] = df['datetime'].apply(lambda x: x.hour)
df['day_of_week'] = df['datetime'].apply(lambda x: x.weekday())
df['is_break'] = df['datetime'].apply(lambda x: x.floor('D') in breaks).astype(int)

df = df[['month', 'day', 'year_after_2021', 'hour', 'day_of_week', 'is_break', 'count']]

df.to_csv("backend/snell_density/data.csv", index=False)

# print(len(lines), " items") #1579308
# print(table)
# print(sum(table[2])) # expect 436 entries on january 3rd