def alternating(a):
    ta = iter(a)

    while 1:
        ta.__next__()

        yield ta.__next__()


list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

for num in alternating(list):
    print(num)