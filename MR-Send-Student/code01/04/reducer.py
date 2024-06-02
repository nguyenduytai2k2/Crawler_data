import sys

current_designation = None
current_salary = 0
for line in sys.stdin:
    key, value = line.strip().split('\t')
    salary = int(value)
    if current_designation == key:
        if current_salary > salary:
            current_salary = salary
    else:
        if current_designation is not None:
            print ('%s\t%s' % (current_designation, current_salary))
        current_designation = key
        current_salary = salary
if current_designation == key:
    print ('%s\t%s' % (current_designation, current_salary))
