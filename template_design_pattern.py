# ABC: Abstract Based Class
from abc import ABC, abstractmethod


class Template(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def func1(self):
        pass

    @abstractmethod
    def func2(self):
        pass

    @staticmethod
    def common_func():
        print('func1, func2 실행')

    def execute(self):
        self.common_func()
        self.func1()
        self.func2()


# 추상메소드를 구현하지 않는 경우 에러 발생
# 바로 에러가 발생하지는 않고 추상클래스를 상속받은 클래스의 객체 생성 시점에 에러가 발생한다.
class TemplateImplementation1(Template):
    def func1(self):
        print('TemplateImplementation1.func1() 호출')

    def func2(self):
        print('TemplateImplementation1.func2() 호출')


class TemplateImplementation2(Template):
    def func1(self):
        print('TemplateImplementation2.func1() 호출')

    def func2(self):
        print('TemplateImplementation2.func2() 호출')


print()

# template_implementation1 = TemplateImplementation1()
# help(template_implementation1)
# template_implementation1.execute()

print('-' * 40)

template_implementation2 = TemplateImplementation2()
# help(template_implementation2)
template_implementation2.execute()
