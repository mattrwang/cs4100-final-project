from FILE_READER import read_files
from DATE_PARSER import tabulate_days

lines = read_files("snell_density/Snell Data")
table = tabulate_days(lines)
# print(len(lines), " items") #1579308
# print(table)
# print(sum(table[2])) # expect 436 entries on january 3rd