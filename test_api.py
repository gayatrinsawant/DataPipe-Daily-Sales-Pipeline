from sources import SOURCES
from extract import read_csv_source

rows = read_csv_source(SOURCES[0])
print(len(rows))
print(rows[0])
print(repr(rows[-1]["order_id"]))