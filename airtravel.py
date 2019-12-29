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


# class ClassMethod:
#     @classmethod
#     def print_name(cls):
#         print('My name is %s' % cls.__class__.__name__)
#

'''
class Flight:
    class_attr = []

    def __init__(self):
        self.class_attr = []

    def add_class_attr(self, number):
        Flight.class_attr.append(number)

    def add_instance_attr(self, number):
        self.class_attr.append(number)


first = Flight()
second = Flight()

first.add_class_attr(5)
print(first.class_attr)
print(Flight.class_attr)
print(second.class_attr)
'''

class Football:
  rule = []


class Baseball:
  rule = []


class Basketball:
  rule = []


class Sports(Football, Baseball, Basketball):
  print(Football.rule)
  print(Baseball.rule)
  print(Basketball.rule)


print(Sports.mro())