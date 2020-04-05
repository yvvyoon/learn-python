def traverse(l):
    for el in l:
        if isinstance(el, list):
            for k in traverse(el):
                yield k
        else:
            yield el


a = [1, 2, 3, [4, 5], 6, [7, [8, [9], 10]]]
b = list(traverse(a))

print(b)

