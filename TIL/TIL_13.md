## 소셜 로그인 구현

### Google

<br>

> *[참고]*
>
> - *https://www.mattbutton.com/2019/01/05/google-authentication-with-python-and-flask/*

<br>

이번 Flask 프로젝트에서 처음으로 소셜 로그인을 적용해보고자 한다. 소셜 로그인 또한 Flask에서 `Flask-Social`이라는 익스텐션을 제공하고 있다.

```
(venv) pip install flask-social
```

<br>

`Flask-Social` 익스텐션을 적용하기 위해 다른 익스텐션도 필요한 것 같다.

```
(venv) pip install flask-sqlalchemy flask-mongoengine
```

<br>

이제 사용할 SNS의 API 라이브러리를 설치한다. 추후에 더 확장하기로 하고 일단 페이스북과 구글만 연동해 볼 것이다.

```
(venv) pip install http://github.com/pythonforfacebook/facebook-sdk/tarball/master
(venv) pip install oauth2client google-api-python-client
```

<br>

각 소셜 로그인을 연동하기 위해서는 해당 프로바이더의 API ID와 Key를 들고 있어야 한다.

Facebook: ``

Google: `https://console.cloud.google.com/apis`

<br>

어... 근데... 참고에 적어 놓은 사이트에서는 구글 사용자 인증 API를 사용할 때 `oauth2client` 익스텐션이 이제 더 이상 사용되지 않아 추천하지 않는다는 말이 있다. 알아 보니 2013년부터 오너십이 불분명해졌고 그 결과 `google-auth`라는 라이브러리로 대체 사용한다고 한다.

그런데 이 포스트의 필자는 `google-auth`보다 `Authlib`의 문서가 더 참고하기 쉽다는 이유로 `Authlib`를 사용한다고 한다. 일단 따라해보자.

<br>

> *[참고]*
>
> - *https://google-auth.readthedocs.io/en/latest/oauth2client-deprecation.html*

<br>

```
(venv) $ pip install authlib google-api-python-client google-auth
```

<br>

먼저, `.flaskenv` 파일에 환경변수들을 설정한다.

```
FN_AUTH_REDIRECT_URI=http://localhost:5000/google/auth
FN_BASE_URI=http://localhost:5000
FN_CLIENT_ID=(발급받은 Client ID)
FN_CLIENT_SECRET=(발급받은 Secret Key)
```

<br>

```
/Users/user/workspace/flask-board-app-yyw/venv/lib/python3.7/site-packages/authlib/client/__init__.py:12: AuthlibDeprecationWarning: Deprecate "authlib.client", USE "authlib.integrations.requests_client" instead.
It will be compatible before version 1.0.
Read more <https://git.io/Jeclj#file-rn-md>
  deprecate('Deprecate "authlib.client", USE "authlib.integrations.requests_client" instead.', '1.0', 'Jeclj', 'rn')
 * Debugger is active!
 * Debugger PIN: 219-732-896
/Users/user/workspace/flask-board-app-yyw/venv/lib/python3.7/site-packages/authlib/client/__init__.py:12: AuthlibDeprecationWarning: Deprecate "authlib.client", USE "authlib.integrations.requests_client" instead.
It will be compatible before version 1.0.
Read more <https://git.io/Jeclj#file-rn-md>
  deprecate('Deprecate "authlib.client", USE "authlib.integrations.requests_client" instead.', '1.0', 'Jeclj', 'rn')
```

하 무슨 에러인지 도통 모르겠다. 100% 완벽히 동일하게 따라치지 않았는데도 내 환경과 맞지 않나보다.

다른 샘플을 찾아봤다.

<br>

> *[참고]*
>
> - *https://realpython.com/flask-google-login/*

<br>

```
(venv) $ pip install requests oauthlib pyOpenSSL
```

<br>

## OAuth2, OIDC(OpenID Connect)

소셜 로그인을 하겠다고 으름장을 놓기만 하고 정작 관련 핵심 개념에 대해 간과하고 있었다. 소셜 로그인에 `OAuth2`, `OIDC`라는 개념이 제일 주요한데 `OIDC`는 `OAuth2` 위에 새로운 아이디어와 개념을 추가하여 개발된 것이다.

써드파티 앱이 클라이언트로서 서버***(Google, Facebook 등의 소셜 로그인 프로바이더)***에 사용자 인증과 관련하여 요청을 보내게 되는데 그 요청-응답 프로세스는 아래와 같다. 이 프로세스는 `OAuth2`가 정의한 `Authorization Code Flow`이다.

<br>

> 1. *내 써드파티 앱을 클라이언트로서 프로바이더에 등록한다.*
> 2. *프로바이더의 인증 URL로 클라이언트의 요청을 전달한다.*
> 3. *프로바이더가 사용자의 인증을 요구한다.*
> 4. *프로바이더가 자신들을 대행하는 클라이언트 써드파티 앱에 사용자가 동의하도록 요구한다.*
> 5. *프로바이더가 클라이언트에게 유니크한 인증 코드를 전송한다.*
> 6. *프로바이더로부터 받은 인증 코드를 다시 프로바이더의 토큰 URL로 전송한다.*
> 7. *사용자를 대신하여 다른 프로바이더의 URL들과 함께 클라이언트에게 토큰을 전송한다.*

<br>

