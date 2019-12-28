def outer_func():
    a = 20

    def inner_func():
        a = 30
        # print('a: %d' % a)
        print(locals())

    inner_func()

    # print('a: %d' % a)
    print(locals())


a = 10

outer_func()

# print('a: %d' % a)
print(locals())
print(globals())
