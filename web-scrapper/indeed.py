# find vs find_all
# find -> 조회한 데이터 중 첫 번째 데이터만
# find_all -> 모든 데이터 조회

import requests
from bs4 import BeautifulSoup

LIMIT = 50
# f는 자바스크립트에서의 백틱과 비슷한 기능을 함
# URL = f'https://www.indeed.com/jobs?q=python&limit={LIMIT}'
URL = f'https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&l=%EC%84%9C%EC%9A%B8&radius=25&limit={LIMIT}'


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
    # 일자리를 추출해서 담을 변수
    jobs = []

    # for page in range(last_page):
    result = requests.get(f'{URL}&start={0 * LIMIT}')
    soup = BeautifulSoup(result.text, 'html.parser')
    results = soup.find_all('div', {'class': 'jobsearch-SerpJobCard'})

    for result in results:
        # ['title'] -> a 태그의 title 속성의 값 가져오기
        title = result.find('div', {'class': 'title'}).find('a')['title']
        company = result.find('span', {'class': 'company'})
        company_anchor = company.find('a')

        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)

        # strip() -> 특정 문자 또는 문자열 제거
        # 현재 코드에서는 공백 및 빈 행 제거
        company = company.strip()

        print(title, company)

    return jobs
