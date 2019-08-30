import random
import requests

# Javascript 버전
# _.range(1, 46)
# _.sampleRange(_.range(1, 46), 6)
# _.sortBy(_.sampleRange(_.range(1, 46), 6))
lotto = sorted(random.sample(range(1, 46), 6))

# Javascript 버전
# axios.get(url)
url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo=1'
res = requests.get(url)
data = res.json()
winner = []

# 파이썬 문법상 '이상, 이하'는 없음
for i in range(1, 7):
    # 자바스크립트의 백틱과 동일한 기능인 f
    winner.append(data[f'drwtNo{i}'])
    
print(lotto)
print(winner)

# 파이썬의 집합 자료형
# 교집합은 &, 합집합은 |
match = len(set(lotto) & set(winner))

print(match)
print()