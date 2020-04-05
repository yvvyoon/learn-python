class Odds:
    def __init__(self, limit=None):
        self.data = -1
        self.limit = limit

    # iterator 객체가 없으면 해당 클래스는 not iterable이기 때문에
    # __next__ 메소드에서 에러 발생
    def __iter__(self):
        return self

    # python2에서는 next(self)로 가능하지만
    # python3에서는 __next__(self)
    def __next__(self):
        self.data += 2

        if self.limit and self.limit <= self.data:
            raise StopIteration

        return self.data


for num in Odds(20):
    print(num)

# print(list(Odds(20)))
