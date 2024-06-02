import sys

header = sys.stdin.readline()
for line in sys.stdin  :
    fields= line.split(',')
    print ('%s\t%d' % ("min", int(fields[5])))
