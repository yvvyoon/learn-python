# Flask framework

## Pagination

Django에서와 마찬가지로 Flask에서도 페이징 처리를 해보자.

`Flask-SQLAlchemy`가 정말 강력하다고 느낀 게 페이징 처리 관련 객체까지도 제공을 해버린다. 데이터 만지는 것과 관련된 모든 기능을 다 가지고 있는 것 같다.

```
>>> user.followed_posts().paginate(1, 20, False).items
```

<br>

> *`paginated()`의 arguments*
>
> - *1부터 시작하는 페이지 번호*
> - *각 페이지별 항목 수*
> - *에러 관련 플래그 argument이고, `True`인 경우 페이지 범위를 넘게 되면 404 에러, `False`인 경우 빈 페이지를 리턴한다.*

<br>

먼저 `config.py` 파일에 여러 설정 변수들을 담아 놓자.

```python
class Config(object):
	...
	ARTICLES_PER_PAGE = 10
```

<br>

URL에 페이지 번호를 사용하는 방식은 대부분 `query string`을 사용한다. 검색어와 유사한 방식이라는 뜻이다. 페이지 번호를 URL에 지정하지 않으면 기본적으로 1로 시작하고, 아래의 예처럼 사용할 수 있다.

<br>

> *1페이지, http://localhost:5000/index*
>
> *1페이지, http://localhost:5000/index?page=1*
>
> *3페이지, http://localhost:5000/index?page=3*
>
> *(페이지 번호가 주어지지 않아도 default가 1이기 때문에 위의 두 1페이지 URL은 동일함)*

<br>

`query string`은 `request.args` 객체를 통해 `query string`으로부터 주어진 argument들에 접근할 수 있다. `index` view에 페이징 처리를 해보자,

```python
@app.route('/')
@app.route('/index')
def index():
    logger.info('Flaboard 메인 접속. index.html 진입')

    # order_by()와 desc()로 내림차순 정렬, 작성일시 기준으로 정렬
    articles = Article.query.order_by(Article.created_datetime.desc()).all()

    # request.args.get()의 첫 번째 인자인 query string에 할당된 값이 page 변수에 저장된다.
    # articles?page=2의 경우 2가 page 변수가 저장되고, 주어지지 않은 경우 default로 1이 저장된다.
    page = request.args.get('page', 1, type=int)
    paginated_articles = articles.paginate(page, app.config['ARTICLES_PER_PAGE'], False)

    # Django와는 다르게 페이징 처리된 객체를 넘길 때 .items를 꼭 써야 한다.
    return render_template('index.html', title='Flaboard', paginated_articles=paginated_articles.items)
```

<br>

전달받은 `article`, `articles`를 템플릿 파일에서 `paginated_article`, `paginated_articles`로 수정하고 페이지 내비게이터도 추가해준다.

```html
<div class="text-center">
  {% if prev_url %}
  <a href="{{ prev_page_url }}">이전</a>
  {% endif %}
  {% if next_url %}
  <a href="{{ next_page_url }}">다음</a>
  {% endif %}
</div>
```

<br>

근데 에러가 나타났다.

<br>

> *AttributeError: 'list' object has no attribute 'paginate'*

<br>

SQLAlchemy를 사용하면서 `all()` 메소드 뒤에 `paginate()` 메소드를 사용해서 발생하는 에러이다. `paginate()`는 list를 받지 않는데, `all()` 메소드는 list로 값을 반환하기 때문이다.

`all()`을 지우면 정상적으로 나타난다.

다음 코드는 이전 버튼, 다음 버튼까지 적용한 HTML이다.

- index.html

```html
<ul class="pagination justify-content-center">
  {% if prev_url %}
  <li class="page-item">
    <a href="{{ prev_url }}" class="page-link">&laquo;</a>
  </li>
  {% else %}
  <li class="page-item disabled">
    <a href="{{ prev_url }}" class="page-link">&laquo;</a>
  </li>
  {% endif %}
  {% for page_number in pagination.iter_pages() %}
  {% if page_number == pagination.page %}
  <li class="page-item disabled">
    <a href="{{ url_for('index', page=page_number) }}" class="page-link">{{ page_number }}</a>
  </li>
  {% else %}
  <li class="page-item">
    <a href="{{ url_for('index', page=page_number) }}" class="page-link">{{ page_number }}</a>
  </li>
  {% endif %}
  {% endfor %}
  {% if next_url %}
  <li class="page-item">
    <a href="{{ next_url }}" class="page-link">&raquo;</a>
  </li>
  {% else %}
  <li class="page-item disabled">
    <a href="{{ next_url }}" class="page-link">&raquo;</a>
  </li>
  {% endif %}
</ul>

...

<ul class="pagination justify-content-center">
  {% if prev_url %}
  <li class="page-item">
    <a href="{{ prev_url }}" class="page-link">&laquo;</a>
  </li>
  {% else %}
  <li class="page-item disabled">
    <a href="{{ prev_url }}" class="page-link">&laquo;</a>
  </li>
  {% endif %}
  {% for page_number in pagination.iter_pages() %}
  {% if page_number == pagination.page %}
  <li class="page-item disabled">
    <a href="{{ url_for('index', page=page_number) }}" class="page-link">{{ page_number }}</a>
  </li>
  {% else %}
  <li class="page-item">
    <a href="{{ url_for('index', page=page_number) }}" class="page-link">{{ page_number }}</a>
  </li>
  {% endif %}
  {% endfor %}
  {% if next_url %}
  <li class="page-item">
    <a href="{{ next_url }}" class="page-link">&raquo;</a>
  </li>
  {% else %}
  <li class="page-item disabled">
    <a href="{{ next_url }}" class="page-link">&raquo;</a>
  </li>
  {% endif %}
</ul>
```

<br>

#### items 사용 여부의 차이

내비게이터 바에 페이지들의 번호를 나타내는 것을 구현하던 중 `items`를 붙이고 안 붙이고의 차이를 발견했다.

라우터 파일에서 템플릿 파일을 렌더링할 때 `paginated_articles.items`와 `paginated_articles`를 전달한다. `paginated_articles.items`는 페이징 처리된 각 페이지별 게시물 리스트이고, `paginated_articles`는 각 페이지의 객체 자체이다. 그렇기 때문에 템플릿 상에서 내비게이터 바에 페이지 번호들을 출력할 때 `paginated_articles.items`로는 `page` 객체에 접근할 수 없다. 말 그대로 각 게시물 리스트이기 때문에 페이지 번호를 가지고 있지 않고, 페이지 객체가 자신의 페이지 번호를 들고 있다.

`iter_pages()` 메소드를 통해 각 페이지 객체를 순회하고 해당 페이지 번호에 접근할 수 있다

<br>

> *paginated_articles.items를 찍어 보면 **<Article 1> <Article 2> <Article 3> ...** 형식으로 각 게시물 클래스의 인스턴스가 나열되고,*
>
> *paginated_articles를 찍어 보면 **<flask_alchemy.Pagination object at 0x111bc06d0>**처럼 페이지 객체 정보가 찍힌다.*

<br>