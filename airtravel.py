# class Flight:
#     def __init__(self, number):
#         print('init')
#         # super().__init__()
#         self._number = number

#     def __new__(cls, number):
#         print('new')

#         return super().__new__(cls)

#     def number(self):
#         # return 'SN060'
#         return self._number


class ClassMethod:
    @classmethod
    def print_name(cls):
        print('My name is %s' % cls.__class__.__name__)
