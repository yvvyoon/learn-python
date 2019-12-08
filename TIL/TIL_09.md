## Class

파이썬에서 클래스 생성은 여타 언어와 다르게 `new` 키워드를 사용하지 않는다.

기본적으로 `SnakeCase`를 사용하는 변수와 함수와 달리 클래스의 네이밍컨벤션은 `CamelCase`를 사용한다.

- airtravel.py

```python
class Flight:
    def __init__(self):
        print('init')
        super().__init__()

    def __new__(cls):
        print('new')

        return super().__new__(cls)

    def number(self):
        return 'SN060'
```

위 코드가 기본적인 클래스와 인스턴스를 생성하는 코드인데 `__init__` 메소드는 `self`, `__new__` 메소드는 `cls`를 argument로 사용하고 있다. 이 부분은 유닛 테스트를 진행하면서 굉장히 많은 의문이 들었다.

결론적으로, `cls`를 argument로 받는 메소드는 클래스 메소드이고, `self`를 argument로 받는 메소드는 인스턴스 메소드이다. 클래스 메소드는 `@classmethod`라는 데코레이터를 사용하여 선언한다.

클래스 메소드는 인스턴스를 따로 선언할 필요 없이 호출할 수 있다.

```python
class ClassMethod:
  @classmethod
  def print_name(cls):
    print('My name is %s' % (cls.__class__.__name__))
```

```
>>> ClassMethod.print_name()
My name is type
```

<br>

```
>>> from airtravel import Flight
>>> f = Flight()
new
init
```

적지 않은 사람들이 `__init__`이 생성자라고 말하는데 생성자가 아니다. `__new__` 메소드가 생성자이다. 위 코드처럼 `f = Flight()`생성자로 객체를 생성하라고 호출받으면 `__new__` 메소드를 호출하여 객체를 생성 및 할당하고, `__new__`메소드가   `__init__` 메소드를 호출하여 객체에서 사용할 값들을 초기화한다.

파이썬에서 일반적으로 클래스를 생성할 때 `__init__` 메소드만 오버라이딩하여 생성이 아닌 객체 초기화에만 이용한다.

<br>

### 정적 메소드

정적 메소드는 클래스에서 직접 접근 및 참조가 가능한 메소드이다. 파이썬에서 정의한 정적 메소드에는 staticmethod와 classmethod가 있는데 staticmethod는 추가되는 argument가 없는 반면, classmethod는 첫 번째 argument로 클래스를 입력한다.

