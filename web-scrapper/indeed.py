import requests
from bs4 import BeautifulSoup

LIMIT = 50
# f는 자바스크립트에서의 백틱과 비슷한 기능을 함
URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'


def extract_indeed_pages():
    result = requests.get(URL)

    # 해당 url의 html 내용 읽기
    # html.parser 이용
    soup = BeautifulSoup(result.text, 'html.parser')

    # class명이 pagination인 div 태그를 모두 찾기
    pagination = soup.find('div', {'class': 'pagination'})

    # 찾은 div 태그 내에서 a 태그 모두 찾기
    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        # 찾은 a 태그 내에서 span 태그 찾기
        # page.find('span')

        # pages 배열에 추가
        # link.find('span').string -> 태그 제외하고 텍스트만 가져오기
        # pages.append(link.find('span').string)

        # 위 코드와 동일
        pages.append(int(link.string))

    # -1 -> 배열의 마지막 요소
    # :-1 -> 마지막 요소 제외
    # 0:5 -> 0번째 ~ 5번째 조회

    # 마지막 페이지 수
    max_page = pages[-1]

    return max_page


def extract_indeed_jobs(last_page):
    for page in range(last_page):
        result = requests.get(f'{URL}&start={page * LIMIT}')

        print(result.status_code)
