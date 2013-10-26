import csv
import sys
f = open('test.csv', 'rb')
f_csv = csv.reader(f)
count = 0
for row in f_csv:
    print row
    count += 1
    if count == 20:
        sys.exit()
