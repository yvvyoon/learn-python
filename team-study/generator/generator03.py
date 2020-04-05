def Odds(limit=None):
    num = 1

    while not limit or limit >= num:
        yield num

        num += 2


odds = Odds(20)

# for i in odds:
#     print(i)


print(list(odds))
