## Django

### 설치

> *디렉토리 생성 후*
>
> **$ python3 -m venv marcoenv**
>
> **$ source marcoenv/bin/activate**
>
> 또는
>
> **$ . marcoenv/bin/activate**
>
> *프롬프트 앞에 (marcoenv)가 붙어 있으면 제대로 virtualenv가 활성화된 것*
>
> *virtualenv 비활성화 -* **activate**
>
> **$ python3 -m pip install --upgrade pip**
>
> **$ pip install django~=2.0.0**

<br>

### 프로젝트 시작

> **$ cd djangogirls**
>
> **$ django-admin startproject mysite .**
>
> *현재 디렉토리에 mysite 프로젝트 생성*

<br>

### 프로젝트 설정

- setting.py
  - Express.js의 app.js 파일 역할과 비슷한 것 같다.

```python
TIME_ZONE = 'Asia/Seoul'

# 호스트 설정
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.pythonanywhere.com']

# 정적 파일 경로 설정
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 데이터베이스 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

<br>

데이터베이스 설정만 했을 뿐이지 아직 생성되지는 않았으므로 생성해주자.

> **$ python manage.py migrate**
>
> *Operations to perform:*
>
>   *Apply all migrations: admin, auth, contenttypes, sessions*
>
> *Running migrations:*
>
>   *Applying contenttypes.0001_initial... OK*
>
>   *Applying auth.0001_initial... OK*
>
>   *Applying admin.0001_initial... OK*
>
>   *Applying admin.0002_logentry_remove_auto_add... OK*
>
>   *Applying contenttypes.0002_remove_content_type_name... OK*
>
>   *Applying auth.0002_alter_permission_name_max_length... OK*
>
>   *Applying auth.0003_alter_user_email_max_length... OK*
>
>   *Applying auth.0004_alter_user_username_opts... OK*
>
>   *Applying auth.0005_alter_user_last_login_null... OK*
>
>   *Applying auth.0006_require_contenttypes_0002... OK*
>
>   *Applying auth.0007_alter_validators_add_error_messages... OK*
>
>   *Applying auth.0008_alter_user_username_max_length... OK*
>
>   *Applying auth.0009_alter_user_last_name_max_length... OK*
>
>   *Applying sessions.0001_initial... OK*

<br>

### 서버 구동

> **$ python manage.py runserver**
>
> *Performing system checks...*
>
> *System check identified no issues (0 silenced).*
>
> *November 20, 2019 - 11:04:22*
>
> *Django version 2.0.13, using settings 'mysite.settings'*
>
> *Starting development server at http://127.0.0.1:8000/*
>
> *Quit the server with CONTROL-C.*

<br>

### MySQL 연동

#### mysqlclient 설치

> **(marcoenv) $ pip install mysqlclient**
>
> *갑자기 에러 발생;;*
>
> *ERROR: Command errored out with exit status 1:*
> *...*

<br>

음 django 공식문서에서 그닥 권장하지 않는 것 같은 pymysql을 설치하라는 글도 있었지만, 더 구글링을 해봤고 openssl을 사용하는 방법을 찾았다.

> **$ brew install openssl**
>
> **(marcoenv) $ LDFLAGS=-L/usr/local/opt/openssl/lib pip install mysqlclient**
>
> *Collecting mysqlclient*
>
>   *Using cached https://files.pythonhosted.org/packages/f8/9b/5db9a03e2088a87c26e3e4d4c7f*
>
> *7e8f4c2dbae610f9521cdfac15755a795/mysqlclient-1.4.5.tar.gz*
> *I*
>
> *nstalling collected packages: mysqlclient*
>
>    *Running setup.py install for mysqlclient ... done*
>
> Successfully installed mysqlclient-1.4.5*

<br>

#### settings.py 수정

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pyboard',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

<br>

#### 모델 생성

- board/models.py

```python
from django.db import models


# 사용자 테이블
class User(models.Model):
    # FK로 참조되는 컬럼은 unique=True 옵션
    user_id = models.CharField(max_length=100, unique=True)
    user_pw = models.CharField(max_length=100)
    user_nm = models.CharField(max_length=50)
    user_grp_num = models.IntegerField()
    signup_dttm = models.DateTimeField()
    info_mdfy_dttm = models.DateTimeField()


# 사용자그룹 테이블
class User_grp(models.Model):
    user_grp_num = models.IntegerField()
    user_grp_nm = models.CharField(max_length=20)


# 게시물 테이블
class Post(models.Model):
    post_num = models.IntegerField(unique=True)
    post_title = models.CharField(max_length=100)
    post_content = models.TextField()
    attch_file_nm = models.CharField(max_length=200)
    view_cnt = models.IntegerField(default=0)
    # to_field : 참조할 컬럼을 명시적으로 지정
    rgst_user_id = models.ForeignKey(
        User, to_field='user_id', on_delete=models.CASCADE)
    rgst_dttm = models.DateTimeField()
    mdfy_dttm = models.DateTimeField()


# 댓글 테이블
class Reply(models.Model):
    post_num = models.ForeignKey(
        Post, to_field='post_num', on_delete=models.CASCADE)
    reply_num = models.IntegerField()
    rgst_user_id = models.ForeignKey(
        User, to_field='user_id', on_delete=models.CASCADE)
    reply_content = models.TextField()
    reply_passwd = models.CharField(max_length=100)
```

<br>

#### 생성한 모델을 Django와 소통

> **$ python manage.py makemigrations**
>
> */migrations/0001_initial.py 파일 생성됨*
>
> **$ python manage.py migrate**
>
> *실제로 DB에 테이블 생성됨*

<br>

```mysql
BEGIN;
--
-- Create model Post
--
CREATE TABLE `board_post` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `post_num` integer NOT NULL UNIQUE, `post_title` varchar(100) NOT NULL, `post_content` longtext NOT NULL, `attch_file_nm` varchar(200) NOT NULL, `view_cnt` integer NOT NULL, `rgst_dttm` datetime(6) NOT NULL, `mdfy_dttm` datetime(6) NOT NULL);
--
-- Create model Reply
--
CREATE TABLE `board_reply` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `reply_num` integer NOT NULL, `reply_content` longtext NOT NULL, `reply_passwd` varchar(100) NOT NULL, `post_num_id` integer NOT NULL);
--
-- Create model User
--
CREATE TABLE `board_user` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `user_id` varchar(100) NOT NULL UNIQUE, `user_pw` varchar(100) NOT NULL, `user_nm` varchar(50) NOT NULL, `user_grp_num` integer NOT NULL, `signup_dttm` datetime(6) NOT NULL, `info_mdfy_dttm` datetime(6) NOT NULL);
--
-- Create model User_grp
--
CREATE TABLE `board_user_grp` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `user_grp_num` integer NOT NULL, `user_grp_nm` varchar(20) NOT NULL);
--
-- Add field rgst_user_id to reply
--
ALTER TABLE `board_reply` ADD COLUMN `rgst_user_id_id` varchar(100) NOT NULL;
--
-- Add field rgst_user_id to post
--
ALTER TABLE `board_post` ADD COLUMN `rgst_user_id_id` varchar(100) NOT NULL;
ALTER TABLE `board_reply` ADD CONSTRAINT `board_reply_post_num_id_169b1b1e_fk_board_post_post_num` FOREIGN KEY (`post_num_id`) REFERENCES `board_post` (`post_num`);
ALTER TABLE `board_reply` ADD CONSTRAINT `board_reply_rgst_user_id_id_7f3ccbfb_fk_board_user_user_id` FOREIGN KEY (`rgst_user_id_id`) REFERENCES `board_user` (`user_id`);
ALTER TABLE `board_post` ADD CONSTRAINT `board_post_rgst_user_id_id_440d704a_fk_board_user_user_id` FOREIGN KEY (`rgst_user_id_id`) REFERENCES `board_user` (`user_id`);
COMMIT;
```

<br>

#### 관리자 계정 생성

> **$ python manage.py createsuperuser**
>
> ...

<br>

#### 앱 생성

> **$ python manage.py startapp board**

<br>

### 관리자 페이지에 board 앱 포함시키기

- board/admin.py

```python
from django.contrib import admin

from .models import Post, Reply

admin.site.register(Post)
admin.site.register(Reply)
```

<br>

