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





