<<<<<<< HEAD
## Flask Framework

=======
## \__name__ 변수

현재 파일이 실행되는 상태 또는 위치를 파악하기 위해 사용하는 변수이다.

모듈의 이름이 저장되는 변수이며 모듈을 불러왔을 때 모듈의 이름이 들어간다.

인터프리터로 해당 모듈 파일을 직접 실행하면 모듈 이름이 아니라 `__main__`이 들어가게 된다. 어떤 파일인지에 관계없이 파이썬 인터프리터가 최초로 실행한 파일에서는 `__main__`이 들어가게 된다.

한 스크립트 파일은 엔트리 포인트가 될 수도 있고 모듈이 될 수도 있다. 다시 말해, 파이썬에서 일반 스크립트 파일과 모듈의 차이가 없다는 뜻이다.

```python
if __name__ == '__main__':
  ...
```

위와 같은 if문을 자주 볼 수 있는데 `__name__` 변수의 값이 `__main__`인지 확인하는 작업을 통해 해당 파일이 엔트리 포인트인지 모듈인지 판단한다. 자바에서의 `public void static main(String args)`와 유사한 역할이다.

<br>

> *"만약 이 파일이 인터프리터에 의해 직접 실행되는 경우"*

<br>

- main.py

```python
print('main.py __name__:', __name__)
```

```
$ python3 main.py

main.py __name__: __main__
```

<br>

- hello.py

```python
print('hello module start')
print('hello.py __name__:', __name__)
print('hello module end')
```

```
$ python3 hello.py

hello module start
hello.py __name__: __main__
hello module end
```

<br>

- main.py

```python
import hello

print('main.py __name__:', __name__)
```

```
$ python3 main.py

hello module start
hello.py __name__: hello
hello module end
main.py __name__: __main__
```

<br>

뭐가 달라졌을까.

스크립트 파일을 호출한 시점에 따라 `__name__` 변수의 값이 달라진 것을 확인할 수 있다. 모듈로서 사용될 때의 `__name__`은 모듈의 이름이 저장되고, 프로그램의 엔트리 포인트로서 사용될 때는 `__main__`이 저장된다.

파이썬을 시작한지 거의 1개월이 다 되어 가는데 이제서야 제대로 이해했다는 게 부끄럽긴 하다. 기초부터 다시 파야할 것이 너무나도 많다.

<br>

## Namespace

프로그래밍 언어에서 모든 변수의 이름을 중복되지 않게 선언하는 것은 쉽지 않다. 게다가 자바에서처럼 변수 또는 함수에 대해 접근제어를 하지 않는다. 파이썬 내부의 모든 것은 객체로 구성되고, 이 객체들은 특정 이름과 매핑되는데 바로 이 매핑을 네임스페이스(Namespace)라는 공간에서 보관하고 있다.

파이썬은 스크립트 언어로서, 여타 컴파일 언어들과 다르게 자동으로 실행되는 메인 함수가 존재하지 않는다. 때문에 스크립트 파일을 실행하면 `Level0 코드(indent가 없는 코드)`부터 순차적으로 수행하고, 별다른 호출이 없으면 함수 및 클래스는 정의만 하고 끝낸다.

아래 코드의 결과로 알 수 있다.

```python
def outer_func():
    a = 20

    def inner_func():
        a = 30
        print('a: %d' % a)

    inner_func()

    print('a: %d' % a)


a = 10

outer_func()

print('a: %d' % a)
```

```
a: 30
a: 20
a: 10
```

<br>

파이썬의 네임스페이스는 아래처럼 분류된다.

- Built-in Namespace

  기본 내장 함수 및 기본 예외 등 파이썬으로 작성된 모든 코드 내의 이름들을 포함한다. 

- Global Namespace

  모듈 별로 존재하는 네임스페이스이고 특정 모듈 내에서 공통적으로 사용될 수 있는 이름들이 소속된다.

- Local Namespace

  함수 및 메소드 별로 존재하는 네임스페이스이고 함수 및 메소드 내의 지역 번수들의 이름들이 소속된다.

<br>

파이썬에서의 네임스페이스는 딕셔너리 형태로 저장되는데 특정 함수 및 메소드 안에서 네임스페이스는 locals()` 함수를 사용하여 확인할 수 있다. 

```python
def outer_func():
    a = 20

    def inner_func():
        a = 30
        
        print(locals())

    print(locals())


a = 10

print(locals())
print(globals())
```

```
{'a': 30}
{'a': 20, 'inner_func': <function outer_func.<locals>.inner_func at 0x100b0c9e0>}
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x100b0dcd0>, '__spec__': N
one, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': 'namespace.py', '__cached__': None, 'outer_func': <function outer_func 
at 0x100b0c0e0>, 'a': 10}
{'__name__': '__main__', '__doc__': None, '__package__': None, '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x100b0dcd0>, '__spec__': N
one, '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': 'namespace.py', '__cached__': None, 'outer_func': <function outer_func 
at 0x100b0c0e0>, 'a': 10}
```

<br>

각 `locals()`를 호출한 구역에 따라 결과가 달라진 걸 확인할 수 있다. `outer_func()`에서는 `inner_func()`와 다르게 변수 a에 20이라는 값이 저장되었고 `inner_func()`에 대한 정보가 담겨져 있다.

마지막 `locals()`는 `globals()`와 동일한 결과를 나타낸다. 모듈 전체 내에서 통용되기 때문에 `__name__` 변수에 `__main__`이 저장된 것을 알 수 있다.