class charic():
    def __init__(self, name, level):
        self.name = name
        self.level = level

    def __str__(self):
        return '닉네임: {}, 레벨: {}'.format(self.name, self.level)


create = charic('Marco', 28)

print(create)
