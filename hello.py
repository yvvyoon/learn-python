name = 'yoon'
age = 28

print(name)

# 파이썬에서는 {}를 쓰지 않고 탭 한번으로 블록을 구분
# 스페이스 4칸이 아님
""" 
멀티라인 코멘트
"""

# 반복
# 1. 단순 반복(while, for)
# 2. 순회(forEach) : 특정 자료를 한 번씩만 조회하면서 반복
#   - 배열, 오브젝트

foods = ['바스버거', '브록시', '고갯마루', '대우식당', '베이징코야', '백운봉막국수', '경천애인']

print(foods[0])
print(foods[-1]) # 마지막 인덱스 조회

# foods.forEach((elem) => {
#     console.log(elem);
# })

for elem in foods: 

if age > 40:
    print('아재') 
else:
    print('오빠')
    
