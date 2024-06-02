import sys

min_salary = sys.maxsize

for line in sys.stdin:
    key, value = line.strip().split('\t')
    salary = int(value)
    if salary < min_salary:
        min_salary = salary

print ("%s\t%s" % ("min", min_salary))