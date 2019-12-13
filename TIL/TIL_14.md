## devpi

`devpi`는 궁극적으로 프로덕션과 같은 외부 환경에 패키지를 배포하기 전에 개발 단계에서 사용자와 개발자 간 패키지를 공유하기 위한 메커니즘을 가진다. 또한 `PyPI`에 빠르고 신뢰할 만한 패키지 캐시를 제공하는 툴이다. `devpi`를 활용하여 `PyPI`가 다운되어도 전혀 영향을 받지 않는 환경을 마련할 수 있으며, 오프라인 상황에서도 파이썬 패키지에 접근할 수 있다. mirror 서버를 구축할 수 있다는 얘기이다.

`devpi`는 서버와 클라이언트 측의 핵심 `devpi` 시스템으로 구성된 3개의 패키지를 제공하고 있다.

<br>

>- **devpi-server**
>
>    pypi.org의 기존 캐싱 인덱스뿐만 아니라 pypi.org로부터 패키지를 상속받아 커스터마이징할 수 있는 사용자 및 팀 기반의 인덱스를 제공
>
>- **devpi-web**
>
>    웹 환경과 검색 인터페이스를 제공하는 devpi-server용 플러그인
>
>- **devpi-client**
>
>    사용자 생성, 인덱스 사용, 인덱스 업로드 및 설치를 위한 하위 커맨드와 `tox`를 호출하기 위한 `test` 커맨드가 포함된 커맨드라인 툴

<br>

### devpi-server 설정

`devpi-server`는 무엇보다도 `PyPI`에 대한 캐싱 프록시 서버 역할을 한다.

내 EC2 인스턴스에 `virtualenv`를 구동한 후 그 안에서 `devpi-server`를 띄우자.

```
(devpi) $ pip install devpi-server
```

<br>

설치 후 서버를 시작하기 전에 `init` 커맨드로 `devpi` 초기화를 해준다.

```
(devpi) $ devpi-init
```

<br>

초기화하면 아래와 같은 구조로 `.devpi` 디렉토리가 생성된다.

```
.devpi
└── server
    ├── .nodeinfo
    ├── .serverversion
    └── .sqlite
```

<br>

이제 `devpi` 서버를 구동한다. IP를 허용해주는 `--host` 옵션을 빼먹지 말자.

```
(devpi) $ devpi-server --start --host=0.0.0.0
```

```
2019-12-12 04:41:26,962 INFO  NOCTX Loading node info from /home/ubuntu/.devpi/server/.nodeinfo
2019-12-12 04:41:26,964 INFO  NOCTX wrote nodeinfo to: /home/ubuntu/.devpi/server/.nodeinfo
/home/ubuntu/devpi/lib/python3.6/site-packages/devpi_server/bgserver.py:31: UserWarning: Use of --start, --stop, --status and --log is deprecated. You should use a process manager of your OS, for example: systemd for Linux, Windows Services, launchd for macOS or http://supervisord.org/
Also see the devpi-gen-config command to create example configuration files for such services.
  "Use of --start, --stop, --status and --log is deprecated. "
starting background devpi-server at http://localhost:3141
/home/ubuntu/.devpi/server/.xproc/devpi-server$ /home/ubuntu/devpi/bin/devpi-server
process 'devpi-server' started pid=23797
devpi-server process startup detected
logfile is at /home/ubuntu/.devpi/server/.xproc/devpi-server/xprocess.log
```

`devpi-server`의 기본 포트는 3141이다. 포트에 대한 귀여운 유래가 있는데, 공식 문서에 따르면 원주율 PI(***3.141***592...)에서 따왔다고 한다. `devpi`에 `PI`가 들어있으니까.

<br>

### devpi-server repository에서 설치 - 로컬

<br>

테스트를 위해 `virtualenv`를 하나 더 만들고 그 안에서 `PyPI` 퍼블릭 repo가 아닌, 내 EC2 인스턴스에서 구동되고 있는 `devpi` repo에서 패키지를 설치해볼 것이다. 

`pip install [패키지명]` 으로 설치하면 파이썬 공식 repo인 `files.pythonhosted.org/packages/...`를 바라보고 패키지를 설치한다. 

```
(playground) python -m pip install --upgrade pip
```

```
(playground) pip install flask
```

```
Downloading
https://files.pythonhosted.org/packages/9b/93/628509b8d5dc749656a9641f4caf13540e2cdec85276964ff8f43bbb1d3b/Flask-1.1.1-py2.py3-none-any.whl (94kB)
```

<br>

`-i` 옵션으로 앞에서 구동한 `devpi` repo에서 패키지를 설치해보자. 접속하는 URL이 다르다.

```
(playground) pip install -i http://localhost:3141/root/pypi/+simple/ flask
```

```
Downloading
http://localhost:3141/root/pypi/%2Bf/45e/b5a6fd193d6cf/Flask-1.1.1-py2.py3-none-any.whl (94kB)
```

<br>

### devpi-server repository에서 설치 - EC2

EC2 내부에서는 테스트가 성공했으므로 내 로컬에서도 테스트를 해보는데 `trusted host` 관련 에러가 발생했다. 찾아보니 커맨드에 `--trusted-host` 옵션을 주거나, `pip.conf` 파일을 생성해서 자동으로 참조하도록 하면 된다.

<br>

- MacOS 환경

```
$ mkdir -p ~/.pip && cat > ~/.pip/pip.conf << EOF

[global]
index-url = http://54.180.29.144:3141/root/pypi/+simple/
trusted-host = 54.180.29.144
[search]
index = http://54.180.29.144:3141/root/pypi/
```

<br>

- Unix 환경

```
$ vim $HOME/Library/Application Support/pip/pip.conf

[global]
index-url = http://54.180.29.144:3141/root/pypi/+simple/
trusted-host = 54.180.29.144
[search]
index = http://54.180.29.144:3141/root/pypi/
```

<br>

- Windows 환경

```
%APPDATA%\pip\pip.ini

[global]
index-url = http://54.180.29.144:3141/root/pypi/+simple/
trusted-host = 54.180.29.144
[search]
index = http://54.180.29.144:3141/root/pypi/
```

<br>

아래는 `PyPI`와 `devpi`의 패키지 다운로드 속도를 비교한 결과이다. 물리적인 거리가 멀기도 하고, 서양권 근무 시작과 겹쳐서 그런지 한국 시각으로 저녁~밤이 되면 유난히 다운로드 속도가 느려진다. 그래서 저녁 8시에 두 repository에 대해 가장 용량이 큰 두 파이썬 패키지로 비교해보았다.

![그림1](https://user-images.githubusercontent.com/12066892/70774381-6f352600-1dbd-11ea-98f5-4886b6223d11.png)

다운로드 속도가 무려 평균 `86.1%`나 절감이 되었다. 저렇게 큰 패키지도 처음 볼 뿐더러 속도차가 이렇게나 많이 날 줄은 몰랐다. 공식 문서에 따르면, 30분마다 캐싱을 한다고 하는데 내부적으로 캐싱 프로세스가 어떻게 이루어지는지에 대해서는 아직 명확하게 파악하지 못했다. 이 부분을 더 공부하면서 mirror 서버 서비스에 대해 깊게 알아봐야겠다.