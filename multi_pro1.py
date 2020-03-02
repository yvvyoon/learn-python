import time

start_time = time.time()


def count(name):
    for i in range(1, 200001):
        print(f'{name}: {i}')


num_list = ['p1', 'p2', 'p3', 'p4']

for num in num_list:
    count(num)

print(f'*** {time.time() - start_time} ***')
