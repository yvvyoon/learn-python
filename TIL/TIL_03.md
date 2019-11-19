## 제어문

#### Practice

#### Q1

다음 코드의 결괏값은 무엇일까?

```python
a = "Life is too short, you need python"

if "wife" in a: print("wife")
elif "python" in a and "you" not in a: print("python")
elif "shirt" not in a: print("shirt")
elif "need" in a: print("need")
else: print("none")
  
# shirt
```

<br>

#### Q2

while문을 사용해 1부터 1000까지의 자연수 중 3의 배수의 합을 구해 보자.

```python
start = 1
sum = 0

while start < 1001:
  if start % 3 == 0:
    sum = start + sum
    
  start += 1
```

<br>

#### Q3

while문을 사용하여 다음과 같이 별(`*`)을 표시하는 프로그램을 작성해 보자.

```python
*
**
***
****
*****

star = 1

while star <= 5:
  print('*' * star)
  
  star += 1
```

<br>

#### Q4

for문을 사용해 1부터 100까지의 숫자를 출력해 보자.

```python
for i in range(1, 101):
  print(i, end = ' ')
```

<br>

#### Q5

A 학급에 총 10명의 학생이 있다. 이 학생들의 중간고사 점수는 다음과 같다.

[70, 60, 55, 75, 95, 90, 80, 80, 85, 100]

for문을 사용하여 A 학급의 평균 점수를 구해 보자.

```python
score = [70, 60, 55, 75, 95, 90, 80, 80, 85, 100]
sum = 0

for i in score:
  sum += i
  
print(sum / len(score))
```

<br>

#### Q6

리스트 중에서 홀수에만 2를 곱하여 저장하는 다음 코드가 있다.

```python
# numbers = [1, 2, 3, 4, 5]
# result = []
# for n in numbers:
#    if n % 2 == 1:
#        result.append(n*2)

result = [num * 2 for num in numbers if num % 2 == 1]

print(result)
```

<br>

## 함수 및 파일 입출력

### 함수 안에서 함수 밖의 변수 변경

```python
# 아래 코드는 함수 외부 변수 a에 아무런 영향을 끼치지 않음
a = 1

def vartest(a):
  a += 1
  
vartest(a)
print(a)
```

```python
# 1. return과 a 변수에 그 결과값 할당을 통해 외부 변수 a 변경
a = 1

def vartest(a):
  a += 1
  
  return a
  
a = vartest(a)
print(a)

# 2. global 변수 사용
def vartest(a):
  global a
	a += 1
  
vartest()
print(a)
```

<br>

### Lambda

함수를 선언하는 def 예약어와 동일한 역할을 하고, def를 사용할 수 없거나 사용하지 않아도 되는 간결하게 만들 상황에서 사용한다.

def와 또 다르게 return 명령어 없이도 값을 반환할 수 있다.

<br>

> lambda 매개변수1, 매개변수2, ...

<br>

```python
add = lambda a, b: a + b

result = add(3, 4)
```

<br>

## 사용자 입출력

자바나 자바스크립트에 비교했을 때 정말 너무 간단하다. 적응이 안될 정도로.

```python
a = input()
b = input('아무거나 입력하세요: ')

# 끝
```

<br>

출력하는 함수인 print 관련 특징은 아래와 같다.

- 따옴표 또는 큰따옴표로 둘러 싸인 문자열은 + 연산과 동일
- 문자열 띄어쓰기는 콤마로

<br>

## 파일 Read & Write

```python
# 파일 생성
f = open('newfile.txt', 'w')
f.close()

# r - 읽기모드
# w - 쓰기모드
# a - 추가모드 (파일 마지막에)
```

<br>

### Write

```python
f = open('./newfile.txt', 'w')

for i in range(1, 11):
    data = '%d번째 줄입니다.\n' % i

    f.write(data)

f.close()
```

<br>

### Read

#### readline()

```python
# 한 줄만
f = open('./newfile.txt', 'r')
line = f.readline()
print(line)
f.close()

# 파일 내용 전부
f = open('./newfile.txt', 'r')

while True:
    line = f.readline()

    if not line:
        break

    print(line)

f.close()

```

<br>

#### readlines()

readlines 함수는 readline과 다르게 파일을 읽은 결과값을 배열로 리턴한다.

```python
f = open('./newfile.txt', 'r')

lines = f.readlines()

for line in lines:
    print(line)

f.close()
```

<br>

#### read()

read()는 파일을 읽은 결과값 전체를 문자열로 리턴한다.

```python
f = open('./newfile.txt', 'r')

data = f.read()
print(data)

f.close()
```

<br>

### Practice

#### Q1

주어진 자연수가 홀수인지 짝수인지 판별해 주는 함수(is_odd)를 작성해 보자.

```python
def is_odd(num):
    if num % 2 == 0:
        print('짝수')
    else:
        print('홀수')

is_odd(3)
```

<br>

#### Q2

입력으로 들어오는 모든 수의 평균 값을 계산해 주는 함수를 작성해 보자. (단 입력으로 들어오는 수의 개수는 정해져 있지 않다.)

```python
def get_avg(*args):
    sum = 0
    result = 0

    for num in args:
        sum += num

    result = sum / len(args)

    print(result)


get_avg(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
```

<br>

#### Q3

다음은 두 개의 숫자를 입력받아 더하여 돌려주는 프로그램이다.

```python
input1 = input("첫번째 숫자를 입력하세요:")
input2 = input("두번째 숫자를 입력하세요:")

total = int(input1) + int(input2)
print("두 수의 합은 %s 입니다" % total)
```

<br>

#### Q4

다음 중 출력 결과가 다른 것 한 개를 골라 보자.

```python
print("you" "need" "python")
print("you"+"need"+"python")
print("you", "need", "python")
print("".join(["you", "need", "python"]))

# 3번째 코드가 다름
-> you need python
```

<br>

#### Q5

다음은 "test.txt"라는 파일에 "Life is too short" 문자열을 저장한 후 다시 그 파일을 읽어서 출력하는 프로그램이다.

이 프로그램은 우리가 예상한 "Life is too short"라는 문장을 출력하지 않는다. 우리가 예상한 값을 출력할 수 있도록 프로그램을 수정해 보자.

```python
f1 = open('test.txt', 'w')
f1.write('Life is too short')
# f1.close()

f2 = open('test.txt', 'r')
print(f2.read())
# f2.close()
```

또는!

```python
with open('test.txt', 'w') as f1:
    f1.write('Life is too short')
with open('test.txt', 'r') as f2:
    print(f2.read())
```

<br>

#### Q6

사용자의 입력을 파일(test.txt)에 저장하는 프로그램을 작성해 보자. (단 프로그램을 다시 실행하더라도 기존에 작성한 내용을 유지하고 새로 입력한 내용을 추가해야 한다.)

```python
a = input()

f = open('new.txt', 'a')
f.write(a)
f.close()
```

<br>

#### Q7

다음과 같은 내용을 지닌 파일 test.txt가 있다. 이 파일의 내용 중 "java"라는 문자열을 "python"으로 바꾸어서 저장해 보자.

```python
fr = open('test.txt', 'r')
result = fr.read()
fr.close()

result = result.replace('java', 'python')

fw = open('test.txt', 'w')
fw.write(result)
fw.close()
```

<br>

### 파이썬 날개달기

- 클래스
- 모듈
- 패키지
- 예외 처리
- 내장 함수
- 외장 함수

<br>

#### Q1

Calculator 클래스를 상속하는 UpgradeCalculator를 만들고 값을 뺄 수 있는 minus 메서드를 추가해 보자. 즉 다음과 같이 동작하는 클래스를 만들어야 한다.

```
class Calculator:
    def __init__(self):
        self.value = 0

    def add(self, val):
        self.value += val


class UpgradeCalculator(Calculator):
    def __init__(self):
        self.value = 0

    def minus(self, val):
        self.value -= val


cal = UpgradeCalculator()
cal.add(10)
cal.minus(7)

print(cal.value)
```

<br>

#### Q2

객체변수 value가 100 이상의 값은 가질 수 없도록 제한하는 MaxLimitCalculator 클래스를 만들어 보자. 즉 다음과 같이 동작해야 한다.

```python
class Calculator:
    def __init__(self):
        self.value = 0

    def add(self, val):
        self.value += val


class MaxLimitCalculator(Calculator):
    def add(self, val):
        self.value += val

        if self.value > 100:
            self.value = 100


cal = MaxLimitCalculator()
cal.add(50)
cal.add(60)

print(cal.value)
```

<br>

#### Q3

