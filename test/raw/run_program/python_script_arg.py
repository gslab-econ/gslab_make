from __future__ import print_function

import sys

with open('test/output/output.csv', 'w') as f:
    for a in sys.argv:
        print(a, file = f)
		
print('Test script complete')