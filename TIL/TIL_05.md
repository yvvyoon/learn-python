### CSRF Token

CSRF(Cross-site Request Forgery)

- 사이트 간 요청 위조
- 사용자의 의도와는 무관하게 공격자가 원하는대로 특정 사이트의 생성, 수정, 삭제 등의 기능을 요청하는 공격

<br>

GET 방식으로 게시물을 등록하다가 POST 방식으로 변경했는데 갑자기 403 Forbidden 에러가 뜨기 시작했다.

>*CSRF 검증에 실패했습니다. 요청을 중단하였습니다.*
>
>Reason given for failure:
>
>​	CSRF token missing or incorrect .

<br>

CSRF token이 없어서 발생하는 에러인데 해결법은 단순하다.

POST를 설정한 form 태그 내에 코드 한줄만 추가하면 끝.

`{% csrf_token %}`

<br>

### url에 파라미터 전달

anchor 태그로 연결된 페이지에 파라미터를 전달하면서 페이지를 이동시키고 싶을 때는 어떻게 해야 할까?

현재 게시판 목록을 조회할 때 html 파일 내에서 Queryset의 all 메소드를 사용하고 있으므로 간편하게 파라미터를 전달할 수 있다.

내가 이동시키고자 하는 url의 이름 뒤에 파라미터를 입력해준다.

```html
<body>
    <h2>{{post.post_title}}</h2>
    &nbsp;&nbsp;&nbsp;
    <p>{{post.rgst_dttm | date:"Y-m-d H:m:s"}}</p>
    <br>
    <p>{{post.post_content}}</p>
    <br><br>
    <a href="{% url 'modify' post.id %}">수정</a>
    <a href="{% url 'delete' post.id %}">삭제</a>
    <a href="{% url 'main' %}">목록으로</a>
</body>
```

<br>

### DRY 원칙

Don't Repeat Yourself

불필요한 로직을 반복하지 말자는 원칙이다.

이를 해결하기 위해서 FBV(Function Baesd View) 또는 CBV(Class Based View)로 구현한다.

<br>

### CBV

현재까지 FBV로 구현했던 코드를 CBV로 구현하여 코드를 최소화하려 한다.

<br>

### 커스텀 사용자 모델

Django에서 기본적으로 제공하는 AbstractBaseUser와 User 클래스를 사용하여 나만의 커스텀 사용자 모델을 만들고자 한다.

email 등의 추가 정보를 넣고 모델을 migrate하기 위해 makemigrations 커맨드를 주면 아래와 같은 에러를 마주치게 된다.

>*django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency user.0001_initial on database 'default'.*

<br>

admin 앱도 AUTH_USER_MODEL에 의존적이다.

이미 board 앱과 admin 앱을 migrate하면서 AUTH_USER_MODEL에 의존성이 생성되었는데, user 앱을 migrate하려니 충돌하는 문제가 발생한 것이다.

admin 앱을 잠시 비활성화시키자. admin 앱 관련 코드만 주석처리하면 된다.

- settings.py

```python
INSTALLED_APPS = [
    'board',
    'user',
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

<br>

- urls.py

```python
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('post/', include('board.urls')),
]
```

<br>

다시 migrate하면 정상적으로 작동할 것이다. 비활성화했던 admin 앱을 재활성화해주자.

재활성화하더라도 기존에 사용했던 관리자 계정은 사라진다.

왜? 커스텀 사용자 모델을 생성하고 migrate했기 때문에. 관리자 계정을 새로 만들어준다.

<br>

Django Form 라이브러리

Django에서는 html 파일에서 사용할 수 있도록 Form 관련 라이브러리를 제공한다.

예로 {{ form. as_p }} 가 있는데 이 한 줄의 코드는 아래의 긴 html 코드와 동일한 역할을 한다.

```html
<div class="panel panel-default registration">
  <div class="panel-heading">
    가입하기
  </div>
  <div class="panel-body">
    <form action="." method="post">
      <input type="hidden" name="csrfmiddlewaretoken" value="SDFHZlmawXy3KhWbQB6rSwqKV3u3houNZDlHP4zMLcNgp2EaKNH3N9K2iXXyOl1P">
      <p>
        <label for="id_email">Email address:</label> <input type="email" name="email" maxlength="254" required="" id="id_email">
      </p>
      <p>
        <label for="id_name">Name:</label> <input type="text" name="name" maxlength="30" id="id_name">
      </p>
      <p>
        <label for="id_password">Password:</label> <input type="text" name="password" maxlength="128" required="" id="id_password">
      </p>
      <div class="form-actions">
        <button class="btn btn-primary btn-large" type="submit">가입하기</button>
      </div>
    </form>
  </div>
</div>
```

<br>

### form 객체

`{% for field in form %}`

field는 BoundField의 인스턴스이다.

> - field.id_for_label : field의 태그에서 사용될 id값으로 보통 id_ + field.name
> - field.initial : 모델에서의 default 속성값
> - field.is_hidden : hidden 속성이 있다면 True, 아니면 False
> - field_errors : field의 유효성을 검증할 때 발견된 에러들
> - field.html_name : 렌더링될 html 태그의 name 속성값
> - field.help_text : 도움말 텍스트
> - field.label : 모델의 verbose_name과 동일한 데이터
> - field_label_tag : field.label을 렌더링한 태그
> - field.name : field의 이름. 폼에 선언된 field의 변수명과 동일함
> - field.value : field에 저장된 실제 데이터

<br>

#### ImproperlyConfigure

리다이렉트될 경로를 지정해주지 않아서 발생하는 에러이다.

해당 폼에서 데이터를 처리한 후 CreateView에서 내부적으로 get_success_url() 메소드를 호출하는데 이 메소드가 참조할 success_url 변수가 없어서 발생한다.

views.py 파일에 success_url 클래스 변수를 선언해주자.

<br>

### LoginView

LoginView는 정상적으로 로그인처리가 완료되면 기본적으로 리다이렉트하는 url이 있는 것 같다.

어떻게 알았냐고? 아래 에러 코드를 보면 Request URL이 내가 처음 보는 경로로 지정되어 있다.

# Page not found (404)

| Request Method: | GET                                     |
| --------------: | --------------------------------------- |
|    Request URL: | http://localhost:8000/accounts/profile/ |

<br>

Using the URLconf defined in `djboard.urls`, Django tried these URL patterns, in this order:

1. admin/
2. post/
3. user/

The current path, `accounts/profile/`, didn't match any of these.

<br>

#### 로그인 리다이렉션 url 설정 방법

- form에 next라는 hidden 필드를 추가하고 '/post/' 값을 기본으로 설정
- form의 action 속성에 '/user/login/?next=/post/' 값 설정
- settings.py 파일에 LOGIN_REDIRET_URL = '/post/' 설정
- LoginView 클래스의 get_success_url() 메소드를 오버라이딩하여 '/post/' 문자열 반환

<br>

### 사용자 인증 middleware

`django.contrib.sesisons.middleware.SessionMiddleware`

SessionMiddleware는 auth_login이라는 로그인 함수를 통해 생성된 세션을 관리한다. 세션 만료 여부를 판단하여 유효할 때에는 request의 session 변수에  session 정보를 저장한다.

`django.contrib.auth.middleware.AuthenticationMiddleware`

AuthenticationMiddleware는 사용자 인증에 관한 처리를 담당하는 미들웨어이다. request.session 값을 사용하여 어떤 사용자인지 확인하고, 확인된 사용자는 request.user 객체에 해당 사용자의 모델 인스턴스를 저장한다.

<br>

