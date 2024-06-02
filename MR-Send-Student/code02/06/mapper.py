import sys

for line in sys.stdin  :
    fields= line.strip().split(',')
    quantity = int(fields[5])
    email = fields[1]
    name = fields[2]
    print ('%s\t%d' % (email+name,quantity ))

