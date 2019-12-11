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

<br>

## 데이터베이스 연동

Flask에서 ORM을 사용할 수 있도록 해주는 `Flask-SQLAlchemy` 익스텐션을 설치하자.

```
(venv) $ pip install flask-sqlalchemy
```

<br>

ORM을 위해 Django 프레임워크에서 기본적으로 `migrate`와 `makemigrations` 커맨드를 제공하는 것과 다르게 Flask에서는 별도의 익스텐션 설치를 필요로 한다. `Flask-Migrate`이다.

```
(venv) $ pip install flask-migrate
```

<br>

연동할 데이터베이스의 접속 정보를 설정하자.

- config.py

```python
import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret!@#'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://yoon:yoon@localhost:3306/flaboard'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

`SQLALCHEMY_TRACK_MODIFICATIONS` 옵션은 데이터베이스에 변경사항이 발생할 때마다 프로그램에 알림을 전달하는 기능에 대한 기능이다. 일단 `False`로.

<br>

이제 `SQLAlchemy` 클래스를 사용하여 데이터베이스 객체와 `migrate` 객체를 생성하자.

- \__init__.py

```python
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
# app.config에 설정된 내용을 참고하여 SQLAlchemy 클래스를 통해 데이터베이스 인스턴스, migrate 인스턴스 생성
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from flaboard import routes, models
```

<br>

이제 테이블과 매핑되는 모델을 생성하자.

- models.py

```python
# 생성한 db 객체를 추가
from flaboard import db


class User(db.Model):
  	# Column 클래스를 각 컬럼으로 인스턴스화
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), index=True, unique=True)
    user_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hashed_password = db.Column(db.String(128))

    # __repr__: 클래스의 객체 텍스트 형식으로 출력할 때 사용되는 메소드
    def __repr__(self):
        return '가입된 회원: {}'.format(self.user_id)
```

<br>

Django에서 `makemigrations`로 모델의 변경사항을 반영했다면, Flask에서는 `Flask-Migrate`에서 사용되는 `Alembic` 마이그레이션 프레임워크를 사용한다. Django에서처럼 `migrations` 디렉토리를 자동으로 생성한다. 이 디렉토리를 생성하기 위해 초기화 커맨드를 수행하자.

```
(venv) $ flask db init
```

```
flask db init  Creating directory /Users/user/workspace/flaboard/migrations ...  done
  Creating directory /Users/user/workspace/flaboard/migrations/versions ...  done
  Generating /Users/user/workspace/flaboard/migrations/script.py.mako ...  done
  Generating /Users/user/workspace/flaboard/migrations/env.py ...  done
  Generating /Users/user/workspace/flaboard/migrations/README ...  done
  Generating /Users/user/workspace/flaboard/migrations/alembic.ini ...  done
  Please edit configuration/connection/logging settings in '/Users/user/workspace/flaboard/migrations/alembic.ini' before proceeding.
```

`migrations` 디렉토리가 생성되고 비어 있는 `versions`가 보인다.

<br>

migrate 하자!

```
(venv) $ flask db migrate
```

```
flask db migrateINFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'user'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_email' on '['email']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_user_id' on '['user_id']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_user_name' on '['user_name']'
  Generating /Users/user/workspace/flaboard/migrations/versions/144a1e4a91b3_.py ...  done
```

migrate를 하면 비로소 `versions` 디렉토리에 생성된 모델의 내역 파일이 나타난다.

<br>

그런데... 아직 DB에 테이블 생성이 반영되지 않았다. 까다롭다 Flask 자식... 커맨드가 추가로 더 필요하다.

```
(venv) $ flask db upgrade
```

```
flask db upgradeINFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 144a1e4a91b3, empty message
```

<br>

`upgrade` 커맨드의 반대인 `downgrade` 커맨드도 제공한다. 이 커맨드는 마지막 migrate를 취소한다. 일종의 Rollback인 셈.

```
(venv) $ flask db downgrade
```

<br>

게시글 테이블인 `Article` 클래스를 생성하고, `User` 클래스와의 관계도 맺어주자.

```python
from flaboard import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), index=True, unique=True)
    user_name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True, unique=True)
    hashed_password = db.Column(db.String(128))
    # backref: 일대다 관계에서 다의 테이블에 추가될 컬럼의 이름
    # 이 프로젝트에서는 각 Article 인스턴스마다 author라는 컬럼이 추가된다.
    # lazy: 어떤 방식으로 쿼리를 날릴 것인지에 대한 옵션
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    
    def __repr__(self):
        return '가입된 회원: {}'.format(self.user_id)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_datetime = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __repr__(self):
        return '제목: {}, 작성자: {}'.format(self.title, self.user_id)
```

<br>

실제로 User 클래스의 인스턴스를 생성하여 사용자를 생성해보자.

```python
from flaboard import db
from flaboard.models import User, Article


new_user = User(user_name='yoon', email='yoon4480@naver.com')
db.session.add(new_user)
db.session.commit()
```

인스턴스를 생성했다고 바로 사용자가 만들어지는 것이 아니라, 각 인스턴스에 대해 `db.session` 객체에 새로운 사용자 인스턴스를 `add` 메소드로 추가하고, `commit`까지 해야 완료된다.

마치 SQL에서 작업하던 방식과 유사한 것 같다. 취소하고 싶다면, `db.session.rollback`하면 된다.

<br>

## 로그인

### 패스워드 해싱

`Werkzeug` 라이브러리를 사용할 것이다. Flask의 핵심적인 의존성을 가지는 라이브러리이기 때문에 별도로 설치하지 않아도 이미 설치되어 있어 바로 사용이 가능하다.

- 기본적인 사용법

```python
from werkzeug import generate_password_hash, check_password_hash

hash = generate_password_hash('mymymy')		# 해시값 어쩌고저쩌고
check_password_hash(hash, 'youryouryour')	# False
```

<br>

### Flask-Login

Django와 크게 다르지 않게 Flask도 로그인 관련 익스텐션을 제공한다. 심지어 **자동 로그인**까지 지원한다. `Remember me`말이다.

```
(venv) pip install flask-login
```

근데 아무리 지지고 볶고 설치해도 제대로 import가 안된다. 인터프리터 문제인가 해서 봤더니 제대로 설정되어 있다. 그래서 일단 Pycharm 설정에서 직접 추가했다.

<br>

다른 익스텐션들과 마찬가지로 앱 인스턴스가 생성될 때 생성 및 초기화되어야 하므로 `__init__.py` 에 추가하고 `LoginManager` 클래스를 임포트한다.

```python
from flask_login import LoginManager

...

login = LoginManager(app)
```

<br>

`Flask-Login` 라이브러리는 4개의 속성들을 필요로 한다.

<br>

> *is_authenticated: Django에서 많은 시행착오를 겪게 했던 그 자식이다.*
>
> *is_active: 특정 사용자의 계정이 유효하면 `True`를 뱉어낸다.*
>
> *is_anonymous: `is_active`와 특별히 뭐가 다른지는 모르겠는데, `is_active`와 반대의 로직을 타는 것 같다.*
>
> *get_id(): 사용자의 ID를 string 형태로 리턴한다. auto_increment인 ID인지 `user_id`인지는 추후에 확인해보도록 하자.*

<br>

프로그래밍에서 다중 상속을 위해 `Mixin`이라는 개념을 사용한다. Django에서 심심치 않게 봐와서 낯설진 않다.

이 `UserMixin`을 뒤져보면 위의  `Flask-Login` 라이브러리가 사용하는 4개의 속성에 대한 메소드들이 정의되어 있다.

- models.py

```python
...
from flask_login import UserMixin

...
class User(UserMixin, db.Model):
  
```

<br>

### User Loader 함수

튜토리얼로부터 이해한 바로는 세션에 현재 로그인되어 있는 사용자의 상태를 저장하여 유지하고자 사용하는데, `Flask-Login` 라이브러리가 데이터베이스와의 아무런 연관이 없다 보니 앱 단에서 string 형태로 리턴하는 `id`값을 사용하여 메모리에 저장하는 것 같다.

쓰고 보니 세션 관리가 맞는 것 같다.

- models.py

```python
from flaboard import db, login
...

@login.user_loader
def load_user(id):
  	# id를 string으로 전달받기 때문에 integer로 캐스팅 필요
    return User.query.get(int(id))
```

<br>

### 로그아웃

로그인에 `login_user()` 메소드를 사용한 것처럼 로그아웃 또한 `logout_user()` 메소드를 사용한다. 쉽다.

```python
...
from flask_login import current_user, login_user, logout_user


@app.route('/logout')
def logout():
    logout_user()

    return redirect(url_for('index'))
```

<br>

템플릿 파일에서 로그인 여부에 따라 화면을 분기하는 건 Django와 유사한데, `Flask-Login` 라이브러리에서 제공하는 `current_user` 클래스를 사용한다.

```html
{% current_user.is_authenticated %}
```

<br>

## Logging 모듈 적용

`fileConfig()`로 configuration 파일을 적용하는 방식을 사용하여 내 프로젝트에 로깅을 적용해보았다. 시행착오가 약간 있었는데, config 파일을 불러오는 경로 지정이 애매했다. 일단 프로젝트 root 디렉토리에 배치했는데 이 부분은 더 연구를 해봐야겠다.

<br>

- flaboard/routes.py

```python
...
import logging
import logging.config
...

logging.config.fileConfig('flaboard_logging.conf')
logger = logging.getLogger('flaboard_logger')

...
logger.info('Flaboard 메인 접속. index.html 진입')

...
logger.info('로그인 화면 접속. login.html 진입')
```

<br>

- flaboard_logging.conf

```
[loggers]
keys=root, flaboard_logger

[handlers]
keys=file_handler

[formatters]
keys=flaboard_formatter

[logger_root]
level=DEBUG
handlers=file_handler

[logger_flaboard_logger]
level=DEBUG
handlers=file_handler
qualname=flaboard_logger
propagate=0

[handler_file_handler]
class=FileHandler
level=DEBUG
formatter=flaboard_formatter
args=('logs/flaboard.log',)

[formatter_flaboard_formatter]
format=%(asctime)s - %(levelname)s - %(message)s
datefmt=
```