# Flask framework

## virtualenv 및 Flask 설치

> **$ python3 -m venv venv**
>
> **$ . venv/bin/activate**
>
> **$ pip install flask**

<br>

Flask는 실행할 때 `FLASK_APP`이라는 환경변수를 설정해줘야 하는데 매번 `flask run`할 때 설정하기 귀찮으니 따로 환경변수를 파일에 저장하는 방법을 이용할 수 있다.

Node.js에서 사용했던 `dotenv` 모듈처럼 Python에도 있다.

```
(venv) $ pip install python-dotenv
```

<br>

## 템플릿 연동

Flask에서 `render_template()` 메소드르 사용하면 `Jinja2` 엔진을 호출하여 템플릿 파일을 렌더링한다. Pycharm을 사용하는 필자의 경우 프로젝트를 생성할 때 템플릿 엔진이 `Jinja2`가 디폴트로 설정되어 있다.

```python
from flask import render_template
from app import app


# 이 데코레이터는 URL과 함수 사이의 연관관계를 생성함
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Yoon'}

    return render_template('index.html', title='Flaboard', user=user)
```

<br>

Django와 마찬가지로 템플릿 언어 `{{ ... }}`가 `render_template()`메소드가 전달하는 argument를 받아 온다.

<br>

## Flask-WTF

CSRF 공격을 막기 위해 `config.py` 파일에 `SECRET_KEY` 변수를 설정하여 암호화한다.

```
(venv) $ pip install flask-wtf 
```

<br>

- config.py

```python
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
```

<br>

`Flask-WTF`을 통해 각 폼에 필요한 필드들을 클래스 변수로 선언한다.

```python
# Flask의 익스텐션은 flask_<name>의 네이밍컨벤션을 따른다.
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    userid = StringField('ID', validators=[DataRequired()])
    password = PasswordField('패스워드', validators=[DataRequired()])
    remember_me = BooleanField('자동 로그인')
    submit = SubmitField('로그인')
```

<br>

`DataRequired` 밸리데이터를 통해 해당 필드가 비어 있는 상태로 전달되지 못하게 방지한다.

<br>

```html
{% extends 'base.html' %}

{% block content %}
    <h1>로그인</h1>
    <form action="" method="POST" novalidate>
        {{ form.hidden_tag() }}
        <p>
            {{ form.userid.label }}
            <br>
            {{ form.userid(size=32) }}
        </p>
        <p>
            {{ form.password.label }}
            <br>
            {{ form.password(size=32) }}
        </p>
        <p>{{ form.remember_me() }} {{ form.remember_me.label }}</p>
        <p>{{ form.submit() }}</p>
    </form>
{% endblock %}
```

<br>

> *novalidate: 브라우저가 이 form에 validation을 처리하지 않도록 하는 속성*
>
> *form.hidden_tag(): CSRF 공격을 방지하는 토큰을 포함하고 있는 hidden 필드를 생성하는 템플릿 argument*

<br>

> *Flask는 기본적으로 코드를 수정하면 서버를 내렸다 다시 올려야 한다. 환경변수를 설정해서 서버 재기동 없이 수정된 코드가 바로 반영되도록 하자.*
>
> *.flaskenv 파일에 아래 코드를 추가한다.*
>
> *FLASK_DEBUG=True*

<br>

- routes.py

```python
...

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    #
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.userid.data, form.remember_me.data))

        return redirect('/index')

    return render_template('login.html', title='로그인', form=form)
```

<br>

`validate_on_submit()` 메소드는 HTTP 요청 메소드에 따라 리턴 값이 다른데, `GET` 메소드의 경우 항상 `False`를 리턴하고 `POST` 메소드의 경우 요구하는 데이터가 모두 채워져 있으면 `True`, 하나라도 결여되면 `False`를 리턴한다.

`flash()` 메소드는 사용자에게 메시지를 보여주는 역할을 하는데, 자동으로 화면에 뿌려지는 방식은 아니다. 화면에 나타내기 위해 템플릿 파일에서 `get_flashed_messages()` 메소드를 사용해야 한다.

 