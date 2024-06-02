import sys

current_count = 0
for line in sys.stdin:
    key, count = line.strip().split('\t')
    if key == 'bill':
        current_count += int(count)


print("%s\t%d"%("bill",current_count))
