class Duck:
    def quack(self):
        print('(꽥꽥)')

    def use_feathers(self):
        print('(퍼덕퍼덕)')


class Person:
    def quack(self):
        print('배고프단 말이다!')

    def use_feathers(self):
        print('(주워서 후후)')


def do_something_in_the_forest(entity):
    entity.quack()
    entity.use_feathers()


def main():
    donald = Duck()
    yoon = Person()

    do_something_in_the_forest(donald)
    do_something_in_the_forest(yoon)


if __name__ == '__main__':
    main()

# EAFP (Easier to ask forgiveness than permission; 하고 나서 용서를 비는 것이 하기 전에 허락을 구하는 것보다 쉽다.)
# 참고: https://ko.wikipedia.org/wiki/덕_타이핑
