## Django Framework

### 로그인/로그아웃

Django에는 일반적인 웹과 관련된 기능은 대부분 구현되어 제공하고 있고, 인증된 사용자만 해당 뷰의 핸들러를 호출할 수 있는 기능도 auth 프레임워크를 통해 제공하고 있다.

FBV에서는 `@login_required` 데코레이터를 핸들러에 wrapping하고, CBV에서는 `LoginRequireMixin` 믹스인을 뷰에 추가해야 한다.

Django에서는 세션 정보를 `django_session` 테이블에 보관하여 관리한다.

세션이 없는 상태에서 글을 작성하려고 하며 로그인 화면으로 넘어간다.

`http://localhost:8000/user/login/?next=/post/register/`

위 url에서 확인할 수 있듯이 `/?next=/post/register/` 이 추가되었고, next 옵션을 통해 로그인 후 글쓰기 페이지로 넘어가게 된다.

<br>

### Session 관리

| Session 백엔드 모듈명                          |                기능                 |
| :--------------------------------------------- | :---------------------------------: |
| django.contrib.sessions.backends.db            |         데이터베이스에 저장         |
| django.contrib.sessions.backends.cache         |             캐시에 저장             |
| django.contrib.sessions.backends.cache_db      | 캐시와 데이터베이스를 병행하여 저장 |
| django.contribsessions.backends.file           |             파일에 저장             |
| django.contrib.sessions.backends.signed_cookie |             쿠키에 저장             |

<br>

- secure cookie 사용
  - `SESSION_COOKIE_SECURE = True`
- session 유효기간 설정 (초 단위)
  - `SESSION_COOKIE_AGE = 10`
- sessionid 이름 변경
  - `SESSION_COOKIE_NAME`을 변경
- 매 사용자 요청마다 request.session 객체의 `cycle_key()` 메소드 호출
  - cycle_key() 메소드를 호출할 때마다 sessionid가 변경되고 그 변경된 값이 쿠키에 저장됨

<br>

#### Session 객체

Django에서는 Session 객체에 기본적으로 세 정보를 딕셔너리 형태로 저장한다.

| key                | 데이터                             |
| ------------------ | ---------------------------------- |
| _auth_user_id      | 사용자 ID                          |
| _auth_user_backend | 로그인 시 사용한 인증 백엔드       |
| _auth_user_hash    | 로그인 시 사용한 비밀번호의 해시값 |

<br>

### CBV로 변환

> **참고**
>
> - *https://wayhome25.github.io/django/2017/03/01/django-99-my-first-project-2/*

FBV로 구현했던 회원가입, 로그인, 로그아웃 등 사용자 인증 관련 view들을 CBV로 변환하고자 한다.

#### ModelForm 작성

- forms.py

```python
from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        # Django가 제공하는 회원가입 관련 폼의 필드명은 정해져 있다.
        fields = ['username', 'email', 'password']


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        # 로그인 시 입력받을 필드를 설정
        fields = ['username', 'password']
```

<br>

#### url 패턴 추가

```python
from django.urls import path, include
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    # path('login/', views.login, name='login'),
    path('login/', views.signin, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('logout/', LogoutView.as_view())
]
```

<br>

#### view 작성

```python
from django.shortcuts import render, redirect
from django.http import HttpResponse
# django가 이미 login이라는 함수를 제공하고 있기 때문에
# 내가 만든 login 함수의 이름을 변경해야 함
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .forms import UserForm
from .forms import LoginForm


def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)

            login(request, new_user)

            return redirect('list')
    else:
        form = UserForm()

        return render(request, 'user/signup.html', {'form': form})
      
      
def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('list')
        else:
            return HttpResponse('다시 로그인하세요.')
    else:
        form = LoginForm()

        return render(request, 'user/login.html', {'form': form})
```

<br>

#### template 작성

기존에 사용했던 input 등의 태그들은 `form.as_p` 객체로 대체한다.

- signup.html

```html
<form action="{% url 'signup' %}" method="POST" class="form-horizontal">
  {% csrf_token %} {{ form.as_p }}
  <hr />
  <br />
  <div class="text-center">
    <button class="btn btn-success" type="submit">등록</button
      >&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="/board/article/"
       ><button class="btn btn-secondary">취소</button></a
      >
  </div>
</form>
```

<br>

- login.html

```html
<form action="{% url 'login' %}" method="POST" class="form-horizontal">
  {% csrf_token %} {{ form.as_p }}
  <hr />
  <br />
  <div class="text-center">
    <button class="btn btn-success" type="submit">로그인</button
      >&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="/user/signup/">처음이신가요?</a>
  </div>
</form>
```

<br>

