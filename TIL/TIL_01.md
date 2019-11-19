## Django

### arguments

```python
def plus(a, b, *args, **kwargs):
  print(args)
  # (3, 4, 5, 6, 7, 8)
  # args는 tuple 형태
  
  print(kwargs)
  # {'key1':'1', 'key2':'2', 'key3':'3'}
  # kwargs는 dictionary 형태

plus(1, 2, 3, 4, 5, 6, 7, 8, key1=1, key2=2, key3=3)
```

- positional argument (*args)
- keyword argument (**kwargs)

<br>

### 객체지향 프로그래밍

```python
class Car():
  wheels = 4
  doors = 4
  windows = 4
  seats = 4
  
porche = Car()
porche.color = 'Red'

ferrari = Car()
ferrari.color = 'Yellow'

mini = Car()
mini.color = 'White'
```

<br>

### Method vs Function

```python
class Car():
  wheels = 4
  doors = 4
  windows = 4
  seats = 4
  
  def start():
    print('This is a method')

def start():
  print('This is a function')
```

<br>

method는 클래스 내에서 동작하는 function이다.

다시 말해 method는 자신을 호출하는 클래스가 있다는 것이고, function의 일종이라고 볼 수 있다.

```python
class Car():
  wheels = 4
  doors = 4
  windows = 4
  seats = 4
  
  def start():
    print('This is a method')

porche = Car()
porche.start()

# TypeError: start() takes 0 positional arguments but 1 was given
```

<br>

파이썬은 모든 메소드를 **self**라는 하나의 argument와 함께 사용하는데, 각 메소드의 첫 번째 argument는 메소드를 호출하는 인스턴스 자신이다.

```python
class Car():
  wheels = 4
  doors = 4
  windows = 4
  seats = 4
  
  def start(pizza):
    print(pizza.color)
    print('This is a method')

porche = Car()
porche.color = 'yellow'
porche.start()

# yellow
# This is a method
```

<br>

### dir()

클래스 내의 모든 것들을 리스트업하여 보여주는 함수이다.

```python
# 
```

<br>

### \__str__

porche.\__str__()를 자동으로 호출한다.

<br>

### \__init__

클래스를 만들었을 때 바로 생성되는 메소드이다. 자바 또는 자바스크립트에서의 생성자와 같은 역할이다.

```python
class Car():
  def __init__(self, **kwargs):
    self.wheels = 4
    self.doors = 4
    self.windows = 4
    self.seats = 4
    self.color = kwargs.get('color', 'black')
    self.price = kwargs.get('price', '$20')

  def __str__(self):
    return f'Car with {self.wheels} wheels'

porche = Car(color='green', price='$40')
print(porche.color, porche.price)

mini = Car()
print(mini.color, mini.price)

# green $40
# black $20
# __init__ 함수에서 color와 price를 이미 설정해놓았기 때문에 객체 생성 시 아무런 argument를 주지 않으면 기본적으로 이미 설정된 속성을 따라감
```

<br>

