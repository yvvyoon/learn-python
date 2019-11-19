## 제어문

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

```

