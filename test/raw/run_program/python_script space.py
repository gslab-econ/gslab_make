from __future__ import print_function

with open('test/output/output.csv', 'w') as f:
    for i in range(11):
        print(i, file = f)
		
print('Test script complete')