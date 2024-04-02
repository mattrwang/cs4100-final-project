from FILE_READER import read_files
from DATE_PARSER import tabulate_days

lines = read_files("backend/snell_density/Snell Data")
table = tabulate_days(lines)
# print(len(lines), " items") # 2956779
# print(table)
# print(sum(table[2])) # expect 1899 entries on january 3rd