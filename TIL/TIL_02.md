## 자료형

### 문자열

```python
a = 'Life is too short, You need Python'
a[0:3]
# 'Lif'
```

<br>

0번 인덱스부터 4번 인덱스까지 잘라냈는데도 'Lif'로 출력되는 이유는 **0 <= a < 3**이기 때문이다.

**'Life'** 전체를 출력하고 싶다면 **a[0:4]**라고 알려줘야 한다.

<br>

```python
a = '20191118Sunny'
date = a[:8]
weather = a[8:]
date
# '20191118'
weather
# 'Sunny'
```

<br>

```python
f'{"hi":>10}'
# 'hi        '

f'{"hi":<10}'
# '        hi'

f'{"hi":^10}'
# '    hi    '

f'{"hi":^9}'
# '   hi    '

y = 3.149518
f'{y:0.4f}'
# 3.1495

f'{y:10.4f}'
# '    3.1495'
```

<br>

#### count()

- 특정 문자 개수 카운트

<br>

#### find()

- 특정 문자 위치 리턴
- -1 리턴

<br>

#### index()

- 특정 문자 위치 리턴
- 에러 발생

<br>

#### join()

- 문자열 삽입

```python
', '.join('abcd')
# 'a, b, c, d'
```

<br>

#### upper()

#### lower()

#### lstrip()

#### rstrip()

#### strip()

#### replace()

#### split()

```python
a = 'Life is too short'
a.split()
# ['Life', 'is', 'too', 'short']

a.split()
```

<br>

### 리스트

#### append()

#### sort()

#### reverse()

#### index()

#### insert()

#### remove(x)

- 리스트에서 첫 번째로 나오는 x를 삭제
- 2개 이상일 경우, 앞의 것 하나만 삭제됨

#### pop()

- 특정 요소를 꺼내고 리스트에서 삭제함

#### count()

#### extend()

- a.extend([4, 5]) == a += [4, 5]

<br>

### Dictionary

#### keys()

#### values()

#### items()

#### get()

#### clear()

#### in

<br>

### 집합(set)

리스트나 튜플과는 다르게 순서가 없고, 중복을 허용하지 않는 자료형이다.

```python
s1 = set([1, 2, 3])
s1
# {1, 2, 3}
s2 = set('Hello')
s2
# {'l', 'H', 'e', 'o'}
```

<br>

#### 교집합

```python
s1 = set([1, 2, 3, 4, 5, 6])
s2 = set([4, 5, 6, 7, 8, 9])
s1 & s2
s1.intersection(s2)
# {4, 5, 6}
```

<br>

#### 합집합

```python
s1 | s2
s1.union(s2)
# {1, 2, 3, 4, 5, 6, 7, 8, 9}
```

<br>

#### 차집합

```python
s1 - s2
s1.difference(s2)
# {1, 2, 3}
```

<br>

#### add

- 집합에 한개씩 추가

#### update

- 집합에 여러 데이터 한꺼번에 추가

#### remove

<br>

## 연습문제

#### Q1

홍길동 씨의 과목별 점수는 다음과 같다. 홍길동 씨의 평균 점수를 구해 보자.

```python
kor = 80
eng = 75
mat = 55
(kor + eng + mat) / 3
```

<br>

#### Q2

자연수 13이 홀수인지 짝수인지 판별할 수 있는 방법에 대해 말해 보자.

```python
a = 13
a % 2
# 나머지가 1이면 홀수, 0이면 짝수
```

<br>

#### Q3

홍길동 씨의 주민등록번호는 881120-1068234이다. 홍길동 씨의 주민등록번호를 연월일(YYYYMMDD) 부분과 그 뒤의 숫자 부분으로 나누어 출력해 보자.

```python
pin = '881120-1068234'
front = f'19{ssn[:6]}
back = ssn[7:]
```

<br>

#### Q4

주민등록번호 뒷자리의 맨 첫 번째 숫자는 성별을 나타낸다. 주민등록번호에서 성별을 나타내는 숫자를 출력해 보자.

```python
pin = '881120-1068234'

pin[7:8]
```

<br>

#### Q5

다음과 같은 문자열 a:b:c:d가 있다. 문자열의 replace 함수를 사용하여 a#b#c#d로 바꿔서 출력해 보자.

```python
a = 'a:b:c:d'
a.replace(':', '#')
```

<br>

#### Q6

[1, 3, 5, 4, 2] 리스트를 [5, 4, 3, 2, 1]로 만들어 보자.

```python
a = [1, 3, 5, 4, 2]
a.sort()
a.reverse()
```

<br>

#### Q7

['Life', 'is', 'too', 'short'] 리스트를 Life is too short 문자열로 만들어 출력해 보자.

```python
a = ['Life', 'is', 'too', 'short']
' '.join(a)
```

<br>

#### Q8

(1,2,3)이라는 튜플에 4라는 값을 추가하여 (1,2,3,4)처럼 만들어 출력해 보자.

```python
a = (1, 2, 3)
b = (4,)
a + b
```

<br>

#### Q9

다음과 같은 딕셔너리 a가 있다. 다음 중 오류가 발생하는 경우는 어떤 경우인가? 그리고 그 이유를 설명해 보자.

```python
a = dict()

a[[1]] = 'python'
# 딕셔너리의 키는 배열이 사용될 수 없다.
```

<br>

#### Q10

딕셔너리 a에서 'B'에 해당되는 값을 추출해 보자.

```python
a = {'A':90, 'B':80, 'C':70}

a.pop('B')
```

<br>

#### Q11

a 리스트에서 중복 숫자를 제거해 보자.

```python
a = [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5]

a = set(a)
```

<br>

#### Q12

파이썬은 다음처럼 동일한 값에 여러 개의 변수를 선언할 수 있다. 다음과 같이 a, b 변수를 선언한 후 a의 두 번째 요솟값을 변경하면 b 값은 어떻게 될까? 그리고 이런 결과가 오는 이유에 대해 설명해 보자.

```python
a = b = [1, 2, 3]
a[1] = 4
print(b)

# a와 b 변수 모두 같은 리스트를 바라보고 있기 때문
```