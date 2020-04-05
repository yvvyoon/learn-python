def fibonacci(a=1, b=1):
    while 1:
        yield a

        a, b = b, a + b


t = fibonacci()
'''
for i in range(11):
    print(t.__next__())  # python3에서 generator는 next() 가지지 않음
'''

for i in fibonacci():
    if i > 100:
        break

    print(i)
