# Bài 1.2:
# File Mapper
import sys

header = sys.stdin.readline()

for line in sys.stdin:
    fields = line.strip().split(',')
    print("%s\t%d" % ("salary", int(fields[5])))

# File Reducer
import sys

max_salary = 0 
min_salary = sys.maxsize

for line in sys.stdin:
    key, value = line.strip().split('\t')
    salary = int(value)
    
    if salary < min_salary:
        min_salary = salary
        
    if salary > max_salary:
        max_salary = salary
        
print("$s\t$s" % ("max_salary", max_salary))
print("$s\t$s" % ("min_salary", min_salary))

# Bài 1.3
# Mapper
import sys

for line in sys.stdin:
    fields = line.strip().split(',')
    deptno = fields[6]
    sal = int(fields[5])
    print("%s\t%d" % (deptno, sal))


# Reducer
import sys

max_salaries = {}

for line in sys.stdin:
    deptno, sal = line.strip().split('\t')
    sal = int(sal)
    
    if deptno in max_salaries:
        max_salaries[deptno] = max(max_salaries[deptno], sal)
    else:
        max_salaries[deptno] = sal

for deptno, max_salary in max_salaries.items():
    print('%s\t%s' % (deptno, max_salary))



# Bài 1.5
# Mapper
import sys

header = sys.stdin.readline()
for line in sys.stdin:
    fields = line.strip().split(',')
    print("%s\t%d" % (fields[3],1))
    
    
# Reducer
import sys
managers = {}

for line in sys.stdin:
    key, value = line.strip().split('\t')
    
    if key in managers:
        managers[key] += 1
        
    else:
        managers[key] = 1

for manager in managers:
    print('%s\t%s' % (manager,managers[manager]))

            
            
# File Mapper
import sys

header = sys.stdin.readline() 

min_cost = float('inf')  

for line in sys.stdin:
    fields = line.strip().split(',')
    cost = float(fields[2])
    if cost < min_cost:
        min_cost = cost
    
print("%.2f" % min_cost)
            
# File Reducer
import sys

min_cost = float('inf') 

for line in sys.stdin:
    cost = float(line.strip())
    if cost < min_cost:
        min_cost = cost

print("%.2f" % ("cost", min_cost))
            
# Mapper
import sys

header = sys.stdin.readline() 
max_cost = 0  

for line in sys.stdin:
    fields = line.strip().split(',')
    cost = float(fields[4])
    if cost > max_cost:
        max_cost = cost
    
print("%.2f" % max_cost)

# Reducer
import sys

max_cost = 0

for line in sys.stdin:
    cost = float(line.strip())
    if cost > max_cost:
        max_cost = cost

print("%.2f" % max_cost)