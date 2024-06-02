import sys

header = sys.stdin.readline()
for line in sys.stdin  :
    fields= line.strip().split(',')
    designation = fields[2]
    salary = int(fields[5])
    print ('%s\t%d' % (designation, salary))
