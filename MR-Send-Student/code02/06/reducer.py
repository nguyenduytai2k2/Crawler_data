import sys


current_customer = None
current_quantity = 0
for line in sys.stdin:
    key, value = line.strip().split('\t')
    quantity= int(value)
    if current_customer == key:
        current_quantity += quantity
    else:
        if current_customer is not None:
            print ('%s\t%d' % (current_customer, current_quantity))
        current_customer = key
        current_quantity = quantity
if current_customer == key:
    print ('%s\t%s' % (current_customer, current_quantity))
