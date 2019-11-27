## Django Framework

### Pagination

`from django.core.paginator import Paginator`

Django에서 제공하는 Paginator 모듈을 사용하면 쉽게 페이징 처리를 할 수 있다.

<br>

- Paginator 메소드

| 입력                            | 출력          | Return 타입                          |
| ------------------------------- | ------------- | ------------------------------------ |
| articles                        | <Page 2 of 6> | <class 'django.core.paginator.Page'> |
| articles.has_next()             | True          | <type 'bool'>                        |
| articles.has_previous()         | True          | <type 'bool'>                        |
| articles.has_other_pages()      | True          | <type 'bool'>                        |
| articles.next_page_number()     | 3             | <type 'int'>                         |
| articles.previous_page_number() | 1             | <type 'int'>                         |
| articles.start_index()          | 11            | <type 'int'>                         |
| articles.end_index()            | 20            | <type 'int'>                         |

<br>

- views.py

```python
def article_list(request):
    articles = Article.objects.all()
    # Paginator 객체 생성
    # 파라미터1: 페이지로 분할될 객체
    # 파라미터2: 한 페이지에 나타날 객체 수
    paginator = Paginator(articles, 5)
    # get() 메소드는 딕셔너리 자료형에서 key로 value를 찾는 역할
    # 이 메소드에서는 페이지의 번호를 호출
    page = request.GET.get('page', 1)

    # get_page(page): 페이지 번호를 받아 해당 번호의 페이지 리턴
    try:
        paginated_articles = paginator.page(page)
    except PageNotAnInteger:
        paginated_articles = paginator.page(1)
    except EmptyPage:
        paginated_articles = paginator.page(paginator.num_pages)

    return render(request, 'board/article_list.html', {'paginated_articles': paginated_articles})
```

<br>

- board/article_list.html
  - 뷰에서 context를 `paginated_articles`로 전달하고 있기 때문에 paginator 관련 태그에만 적용하는 게 아니라 기존에 QuerySet 객체를 뿌려주던 코드에서도 `articles`가 아닌 `paginated_articles`로 뿌려줘야 함
  - 이것 때문에 게시글이 출력이 안돼서 삽질 좀 했다. :(

```html
<ul class="pagination justify-content-center">
  {% if paginated_articles.has_previous %}
  <li class="page-item">
    <a class="page-link" href="?page={{ paginated_articles.previous_page_number }}">Prev</a>
  </li>
  {% else %}
  <li class="disabled">
    <span class="page-link">Prev</span>
  </li>
  {% endif %}
  {% for i in paginated_articles.paginator.page_range %}
  {% if paginated_articles.number == i %}
  <li class="active">
    <span class="page-link">{{ i }}
      <span class="sr-only">(current)</span>
    </span>
  </li>
  {% else %}
  <li class="page-item">
    <a class="page-link" href="?page={{ i }}">{{ i }}</a>
  </li>
  {% endif %}
  {% endfor %}
  {% if paginated_articles.has_next %}
  <li class="page-item">
    <a class="page-link" href="?page={{ paginated_articles.next_page_number }}">Next</a>
  </li>
  {% else %}
  <li class="disabled">
    <span class="page-link">Next</span>
  </li>
  {% endif %}
</ul><br>
{% endif %}

...

<table class="table table-hover">
  <thead>
    <th>번호</th>
    <th>제목</th>
    <th>작성자</th>
    <th>작성일시</th>
  </thead>
  <tbody>
    {% for paginated_article in paginated_articles %}
    <tr>
      <td style="width: 5%;">
        <a style="color: black;" href="/article/{{ paginated_article.id }}/">{{ paginated_article.id }}</a>
      </td>
      <td style="width: 30%;"><a style="color: black;" href="/article/{{ paginated_article.id }}/">{{ paginated_article.title }}
        [{{ paginated_article.comments.count }}]</a></td>
      <td style="width: 10%;">{{ paginated_article.author }}</td>
      <td style="width: 10%;">{{ paginated_article.rgst_dttm | date:'Y-m-d H:m:s' }}</td>
    </tr>
    {% endfor %}
  </tbody>
</table>
```

<br>

### pylint 에러

iMac에 새로 개발환경을 구축하고나니 이상하게 자꾸 django 모듈들이 정상적으로 임포트되지 않는다고 계속 빨간줄 에러가 뜬다.

Node.js 할 땐 eslint 패키지 설치했던 기억이 있는데 pylint는 이상하게 안 찾아진다.

>  *Unable to import 'django........' pylint(import-error)*

<br>

.pylintrc의 init-hook에 path를 추가하면 해결할 수 있다고 하는데 내 환경에서는 아직 해결되지 않았다.

```
init-hook='import sys; sys.path.append("c:/a/programming/python/spider_blogupdater/src");
sys.path.append("c:/a/envs/spider3/Lib/site-packages");
sys.path.append("c:/a/envs/spider3/Lib")'
```



