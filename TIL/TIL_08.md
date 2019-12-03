## 목차

- ### [테스트 수행](#테스트-수행)

- ### [폼 테스트](#폼-테스트)

- ### [모델 테스트](#모델-테스트)

- ### [뷰 테스트](#뷰-테스트)

- ### [테스트 코드 커버리지 체크](#100%-Coverage)

<hr>

## Unit test on Django Framework

Django에서는 자동으로 테스트를 수행하는 테스트 프레임워크를 제공한다.

개발자가 직접 수동으로 수행하는 테스트보다 자동 테스트가 주는 이점은, 일단 내 프로그램의 첫 번째 고객으로서의 역할을 할 수 있다는 것이다. 테스트케이스만 잘 설정한다면, 심지어 사람인 고객이 직접 테스트하는 것보다 정확한 테스트 결과를 도출해낼 수 있을 것이다.

<br>

- Unit tests

  클래스나 함수 레벨로 수행하는 독립적인 기능이 잘 동작하는지 검증

- Regression tests

  기존에 발생했던 버그들이 잘 수정되었는지 재검증

- Integration tests

  유닛 테스트를 진행했던 독립적인 각 컴포넌트들의 상호작용을 검증

<br>

> ***SimpleTestCase***
>
> ***TransactionTestCase***
>
> ***TestCase***
>
> ***LiveServerTestCase***

<br>

위의 각 테스트 클래스들은 검증 결과를 True, False인지 또는 두 리턴값들이 동일한지를 검증하기 위해 `assert()` 메소드를 사용한다.

이 중 `TestCase` 클래스가 Django가 제공하는 테스트 프레임워크 중 가장 기본에 해당한다.

<br>

built-in test discovery를 이용하여 유닛 테스트를 진행하게 되는데 `test_*.py`의 패턴을 가진 모든 파일들을 검증한다.

테스트를 수행할 때 프로젝트 디렉토리의 `tests.py` 파일만 테스트하는 것으로 보인다. 그렇기 때문에 `tests.py`를 삭제하고, 각 앱 디렉토리 하위에 `tests` 디렉토리를 생성하고 아래와 같은 구조로 구성한다.

```
board/
	/tests/
  	__init__.py
  	test_models.py
  	test_views.py
  	test_forms.py
```

<br>

TestCase 클래스를 상속받아 커스텀 테스트 클래스 작성

```python
class YourTestClass(TestCase):
  	@classmethod
    def setUp(self):
        # Setup run before every test method.
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_something_that_will_pass(self):
        self.assertFalse(False)

    def test_something_that_will_fail(self):
        self.assertTrue(False)
```

<br>

- `setUpTestData()`

  해당 테스트 클래스 내부에서 변경되지 않을 객체들을 생성하는 역할을 하고 테스트 시작 시, 다시 말해서 클래스 호출 시 한 번만 수행한다.

- `setUp()`

  각 테스트 메소드가 호출될 때마다 호출되는 메소드이다.

  setUpTestData() 메소드와는 반대로 테스트 중 변경될 수 있는 객체를 생성

- `assert***()`

  해당 테스트 조건이 참, 거짓 또는 동일한지 검증하는 메소드

  - `assertTrue()`, `assertFalse()`, `assertEqual()`, `assertRedirects()`, `assertTemplateUsed()` 등

<br>

### 테스트 수행

> **$ ./manage.py test**
>
> *Creating test database for alias 'default'...*
>
> *System check identified no issues (0 silenced).*
>
> *setUpTestData: Run once to set up non-modified data for all class methods.*
>
> *setUp: Run once for every test method to setup clean data.*
>
> *Method: test_false_is_false.*
>
> *.setUp: Run once for every test method to setup clean data.*
>
> *Method: test_false_is_true.*
>
> *.setUp: Run once for every test method to setup clean data.*
>
> *Method: test_one_plus_one_equals_two*
>
> 
>
> *Ran 3 tests in 0.001s*

<br>

테스트 수행에 대해 더 많은 정보를 출력하고 싶다면 `--verbosity 2` 옵션을 주면 된다.

레벨의 기본값은 1이며, 0, 1, 2, 3이다.

<br>

### 폼 테스트

- test_forms.py

> *forms.py 파일을 사용하는 방식으로 커스터마이징 후 테스트 진행*

<br>

### 모델 테스트

- test_models.py

```python
from django.test import TestCase

from board.models import Article, Comment


class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Article.objects.create(title='테스트 코드')

    def test_title_label(self):
        article = Article.objects.get(id=1)
        field_label = article._meta.get_field('title').verbose_name

        # self.assertEquals(field_label == 'titl e')
        # 후자의 경우 테스트가 실패한다면 실제로 테스트 대상 객체를 출력해주기 때문에 용이함
        self.assertEquals(field_label, '제목')

    def test_title_max_length(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('title').max_length

        self.assertEquals(max_length, 100)

    def test_content_label(self):
        article = Article.objects.get(id=1)
        field_label = article._meta.get_field('content').verbose_name

        self.assertEquals(field_label, '내용')

```

<br>

### 뷰 테스트

- test_views.py

```python
from django.test import TestCase
from django.urls import reverse

from board.models import Article, Comment


class ArticleListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_articles = 15

        for article_id in range(number_of_articles):
            Article.objects.create(
                title=f'Title {article_id}'
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/board/list/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)

    def test_view_users_correct_template(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'board/article_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('articles'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['article_list']) == 10)

    def test_lists_all_authors(self):
        response = self.client.get(reverse('articles')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['article_list']) == 3)
```

<br>

#### UnorderedObjectListWarning

테스트를 수행하니 `UnorderedObjectListWarning`라는 경고가 튀어나왔다.

해석 그대로 QuerySet 객체를 ordering되지 않은 상태로 출력하려니 발생하는 경고 메시지이다.

사용 중인 모든 QuerySet 관련 메소드에 `order_by`절을 추가해준다.

```python
articles = Article.objects.all.order_by('id')

# 아래 코드도 동일하게 동작함
# articles = Article.objects.get_queryset().order_by('id')
```

<br>

### 테스트 코드 Coverage 확인

#### coverage 설치

> **$ pip install coverage**

<br>

#### coverage 설정

Coverage.py의 default 설정 파일인 `.coveragerc`를 생성하여 아래와 같이 작성해준다.

```
[run]
source = .

[report]
fail_under = 100			// 설정한 percentage 이하의 코드는 모두 fail
show_missing = True		// 테스트가 수행되지 않은 코드의 라인 넘버 출력
skip_covered = True		// 100% 커버리지를 달성한 소스코드 생략
```

<br>

#### 템플릿 파일 coverage 확인

소스코드 뿐만 아니라 템플릿 파일도 테스트할 수 있는 플러그인을 제공하고 있다.

> **$ pip install django_coverage_plugin**

<br>

설치 후 `.coveragerc` 파일을 열어 `[run]` 헤더 아래에 플러그인을 추가해준다.

```
[run]
source = .
plugins = django_coverage_plugin

...
```

<br>

#### 이전에 수행한 coverage 기록 삭제

> **$ coverage erase**

<br>

#### coverage와 테스트 수행

> **$ coverage run manage.py test**

<br>

#### 테스트 코드 coverage 확인

> **$ coverage report**

<br>

그런데! 매번 이전 기록 지우고, 테스트 돌리고, 리포팅하는 커맨드를 일일히 쳐주기 귀찮다. 쉘 스크립트로 만들어버리자.

- test.sh

```shell
#!/bin/sh

set -e

echo 'Start erasing previous coverage result'
coverage erase

echo 'Start running test with coverage'
coverage run manage.py test

echo 'Start reporting coverage result'
coverage report

echo 'Start generating an HTML report'
coverage html
```

<br>

리포트를 HTML 파일로 생성해주기도 하기 때문에 웹에서도 결과를 확인할 수 있다.

`/htmlcov/index.html` 경로로 접속하고, 각 테스트 대상 소스코드 파일을 클릭하면 어느 코드 라인이 제외되었는지까지 확인할 수 있다. Amazing!