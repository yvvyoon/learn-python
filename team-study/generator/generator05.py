def traverse(t):
    if not isinstance(t, list):
        return [t]

    result = []

    for el in t:
        result.extend(traverse(el))

        # print(traverse(el))

    return result


a = [[1, 2, 3], 4, 5, [6, 7], [8, 9, 10]]
b = traverse(a)

print(b)