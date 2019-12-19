# Flask framework

## OAuth2, OIDC(OpenID Connect)

소셜 인증을 하겠다고 으름장을 놓기만 하고 정작 관련 핵심 개념에 대해 간과하고 있었다. 소셜 인증에 `OAuth2`, `OIDC`라는 개념이 제일 주요한데 `OIDC`는 `OAuth2` 위에 새로운 아이디어와 개념을 추가하여 개발된 것이다.

써드파티 앱이 클라이언트로서 서버***(Google, Facebook 등의 소셜 인증 프로바이더)***에 사용자 인증과 관련하여 요청을 보내게 되는데 그 요청-응답 프로세스는 아래와 같다. 이 프로세스는 `OAuth2`가 정의한 `Authorization Code Flow`이다.

<br>

> 1. *애플리케이션을 클라이언트로서 프로바이더에 등록한다.*
> 2. *프로바이더의 인증 URL로 클라이언트의 요청을 전달한다.*
> 3. *프로바이더가 사용자의 인증을 요구한다.*
> 4. *프로바이더가 자신들을 대행하는 클라이언트 애플리케이션에 사용자가 동의하도록 요구한다.*
> 5. *프로바이더가 클라이언트에게 고유한 인증 코드를 전송한다.*
> 6. *프로바이더로부터 받은 인증 코드를 다시 프로바이더의 토큰 URL로 전송한다.*
> 7. *사용자를 대신하여 다른 프로바이더의 URL들과 함께 클라이언트에게 토큰을 전송한다.*

<br>

## 소셜 인증 구현

진짜 소셜 인증 너무 힘들다. 도대체 얼마나 많은 구글링을 하고 얼마나 많은 튜토리얼들을 뒤졌는지 모른다. 그런데 하나도 적용이 안된다. 나름 내 환경에 맞춘다고 맞췄는데도 안 돌아가고, 아마도 근본적인 원인은 액세스 토큰 등 OAuth 인증 프로세스에 대한 전반적인 이해가 부족하기 때문일 것이다.

그러던 와중에, Miguel 아저씨의 다른 글을 발견했다. 왜 이제서야 나타난 걸까. 14년도 글이지만 OAuth2 모듈을 쓰는 것 같고, `OAuth`가 `OpenID`를 대체했다는 서두로 보아 일단 참고해볼 만한 것 같다. 다시 해보자.

<br>

> *https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask*

<br>

친절하게도 서론에 소셜 인증의 대략적인 흐름이 목록화되어 쓰여 있다. 위에서 7단계로 나열한 프로세스를 참고하면서 리마인드하자.

<br>

> 1. *http://www.example.com/authorize/facebook과 같은 링크로 라우팅해주는 'Facebook으로 로그인' 등의 버튼을 클릭한다.*
>
> 2. *서버는 요청을 수신하고, Facebook의 OAuth 인증 URL로 리다이렉트시킨다.* 
>
>     *(모든 OAuth 프로바이더들은 사용자들에게 리다이렉트할 URL을 문서화해야 한다.)*
>
> 3. *이제 사용자에게 Facebook에 로그인하라는 메시지가 표시된다. 정보 제공 요청 화면이 나타난다. Facebook과 사용자 간의 프라이빗한 트랜잭션이 완료된 것이다. 해당 애플리케이션은 아직 관여되지 않았다.*
>
> 4. *사용자가 정보 제공 요청을 허용하면, Facebook은 http://www.example.com/callback/facebook과 같은 사전에 설정된 콜백 URL로 리다이렉트시킨다. 리다이렉트 URL의 쿼리 스트링에는 애플리케이션이 사용자를 대신하여 Facebook API 액세스에 필요한 권한 코드가 포함되어 있다.*
>
>     *(여기서의 권한 코드는 액세스 토큰을 말하는 것 같다.)*
>
> 5. *이제 애플리케이션은 Facebook API를 사용하여 사용자 정보를 얻는다. 사용자의 고유 식별자로 애플리케이션의 데이터베이스에 사용자 정보를 등록하는데에 사용할 수 있으며, 일단 사용자가 로그인하기 위해 등록되면 사용할 수 있다.*  

<br>

`OAuth`는 주로 `OAuth 1.0a`와 `OAuth 2`, 두 버전이 가장 많이 사용되고 Twitter에서 전자, Facebook에서 후자의 버전을 사용한다. `OAuth 2`는 이전 버전의 기능들을 일부 제거했고 https에 관련된 기능들이 추가되어 이전 버전과 호환되지 않는다.

그런 다음 각 OAuth 프로바이더의 개발자 페이지에서 앱을 만들고 클라이언트 ID와 Secrey Key를 발급받는다.

데이터베이스의 `User` 테이블에 소셜 ID가 들어갈 컬럼을 생성해주고, `OAuth` 클라이언트 패키지 중 `Rauth`를 사용한다. 

```
(venv) $ pip install rauth
```

<br>

### Facebook 인증

튜토리얼에는 Twitter와 Facebook 인증에 대해 안내하고 있는데, 일단 Facebook 인증부터 시작한다. 위에서 언급했듯이 Facebook은 Twitter가 `OAuth 1.0a` 프로토콜을 사용하는 것과 달리 `OAuth 2` 프로토콜을 사용한다.

```python
class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}

            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider

        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    pass
```

<br>

`authorize()`, `callback()` 메소드는 `OAuthSignIn` 클래스를 상속받는 `FacebookSignIn` 클래스에서 오버라이딩한다. 각 프로바이더별 하위 클래스의 베이스가 되는 `OAuthSignIn` 클래스는 모든 OAuth 프로바이더들에게 공통적인 두 핵심 이벤트를 제공한다.

<br>

> 1. *인증 프로세스를 시작하기 위해 애플리케이션은 사용자가 인증하기 위해 프로바이더의 웹사이트로 리다이렉트해야 한다. 이는 `authorize()` 메소드로 한다.*
> 2. *인증이 완료되면 프로바이더는 `callback()` 메소드를 통해 다시 애플리케이션으로 리다이렉트시킨다. 프로바이더는 애플리케이션 내부의 메소드에 직접 접근하지 않기 때문에 `callback()` 메소드를 호출할 URL로 리다이렉트한다. 이 URL은 프로바이더의 명칭을 포함하는 `get_callback_url()` 메소드로 얻을 수 있다.*

<br>

`get_provider()` 클래스 메소드는 프로바이더 명칭이 지정된 `OAuthSignIn` 인스턴스를 찾는데에 사용된다. 검사를 통해 `OAuthSignIn`를 상속한 모든 하위 클래스(FacebookSignIn, TwitterSignIn)를 찾은 다음 각 인스턴스를 딕셔너리로 저장한다.

<br>

`FacebookSignIn` 클래스의 바디를 채우자.

```python
class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        # provider_name을 facebook으로 초기화
        super(FacebookSignIn, self).__init__('facebook')

        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com'
        )
```

<br>

`authorize_url`과 `access_token_url`은 인증 과정에서 애플리케이션에 대해 Facebook에서 정의한 URL이고, `base_url`은 Facebook API 호출에 대한 prefix URL이다. 이 정보들은 프로바이더 간에 표준화된 것이 아니기 때문에 각 프로바이더의 문서를 참고해야 한다.

(표준화 좀 해주세요 ㅠㅠ)

<br>

- routes.py

```python
from flaboard.oauth import OAuthSignIn


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)

    return oauth.authorize()
```

<br>

아래 코드는 인증 완료 후 리다이렉트할 콜백 라우트 메소드이다.

- routes.py

```python
@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))

    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()

    if social_id is None:
        flash('인증 실패.')

        return redirect(url_for('index'))

    user = User.query.filter_by(social_id=social_id).first()

    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()

    login_user(user, True)

    return redirect(url_for('index'))
```

<br>

- oauth.py

```python
class OAuthSignIn(object):
  ...
  
  def callback(self):
    def decode_json(payload):
      return json.loads(payload.decode('utf-8'))

    if 'code' not in request.args:
      return None, None, None

    oauth_session = self.service.get_auth_session(
      data={
        'code': request.args['code'],
        'grant_type': 'authorization_code',
        'redirect_uri': self.get_callback_url()
      },
      decoder=decode_json
    )

    me = oauth_session.get('me').json()

    return (
      'facebook$' + me['id'],
      # facebook은 따로 사용자명을 사용하지 않기 때문에 이메일 주소 앞부분을 split
      me.get('email').split('@')[0],
      me.get('email')
    )
```

<br>

프로바이더는 `callback()` 메소드를 통해 애플리케이션이 프로바이더의 API에 액세스할 수 있도록 인증 토큰을 전달한다. `OAuth 2`에서는 `code` argument가 인증 토큰이고, `OAuth 1.0a`에서는 `oauth_verifier` argument가 인증 토큰이다. 

<br>



