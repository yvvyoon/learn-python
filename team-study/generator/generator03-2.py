from itertools import *


list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for num in islice(list, 1, 7, 2):
    print(num)