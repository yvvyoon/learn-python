## Flask app to Docker image

### 이미지 생성

Flask 앱이 준비되어 있고 docker가 설치되어 있다는 전제 하에 진행한다. Flask 앱의 root 디렉토리로 먼저 이동한다. 빌드할 우리의 앱을 `-t, --tag` 옵션을 줘서 `flaboard:latest`라는 이름의 태그를 설정하고 빌드하는 커맨드이다.

```
$ docker build -t flaboard:latest .
```

```
unable to prepare context: unable to evaluate symlinks in Dockerfile path: lstat /Users/user/workspace/flask-board-app-yyw/Dockerfile: no such file or directory
```

<br>

docker 이미지로 빌드하기 위해서는 `Dockerfile` 파일이 필요하다. 위 에러는 `Dockerfile`이 없어서 발생하는 것이다.

```
$ touch Dockerfile
```

```dockerfile
# Dockerfile

FROM python:3.7.5

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]
```

<br>

```
$ docker build -t flaboard:0.1 .
```

```
Sending build context to Docker daemon  146.8MB
Step 1/6 : FROM python:3.7.5
 ---> fbf9f709ca9f
Step 2/6 : COPY . /app
 ---> 8d94f3f0f6a4
Step 3/6 : WORKDIR /app
 ---> Running in aa662debe7ed
Removing intermediate container aa662debe7ed
 ---> 2a09eae0592e
Step 4/6 : RUN pip install -r requirements.txt
 ---> Running in 1620ec99123c
Collecting alembic==1.3.1
  Downloading https://files.pythonhosted.org/packages/84/64/493c45119dce700a4b9eeecc436ef9e8835ab67bae6414f040cdc7b58f4b/alembic-1.3.1.tar.gz (1.1MB)
Collecting astroid==2.3.3
  Downloading https://files.pythonhosted.org/packages/ad/ae/86734823047962e7b8c8529186a1ac4a7ca19aaf1aa0c7713c022ef593fd/astroid-2.3.3-py3-none-any.whl (205kB)
Collecting Authlib==0.13
  Downloading https://files.pythonhosted.org/packages/f7/14/133f67ec0be1ddc2679bbe4e8198fb32a354ef4a5b314268a51417b65cfd/Authlib-0.13-py2.py3-none-any.whl (216kB)
Collecting autopep8==1.4.4
  Downloading https://files.pythonhosted.org/packages/45/f3/24b437da561b6af4840c871fbbda32889ca304fc1f7b6cc3ada8b09f394a/autopep8-1.4.4.tar.gz (114kB)
Collecting Babel==2.7.0
  Downloading https://files.pythonhosted.org/packages/2c/60/f2af68eb046c5de5b1fe6dd4743bf42c074f7141fe7b2737d3061533b093/Babel-2.7.0-py2.py3-none-any.whl (8.4MB)
Collecting blinker==1.4
  Downloading https://files.pythonhosted.org/packages/1b/51/e2a9f3b757eb802f61dc1f2b09c8c99f6eb01cf06416c0671253536517b6/blinker-1.4.tar.gz (111kB)
  
...
  
Removing intermediate container 1620ec99123c
 ---> 988bc9cc90dd
Step 5/6 : ENTRYPOINT ["python"]
 ---> Running in d8e8a52b2f25
Removing intermediate container d8e8a52b2f25
 ---> 2ea5524a699a
Step 6/6 : CMD ["app.py"]
 ---> Running in 879a09188a0f
Removing intermediate container 879a09188a0f
 ---> ef9b5b747b7b
Successfully built ef9b5b747b7b
Successfully tagged flaboard:latest
```

<br>

엄청나게 많은 로딩 게이지들과 프로세스가 지나고 나서 마지막에 `Successfully built ef9b5b747b7b`와 `Successfully tagged flaboard:latest` 메시지만 뜨면 된다. 반가워라.

이미지가 잘 빌드되었는지 확인해보자. 생각보다 용량이 크다.

```
$ docker images
```

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
flaboard            latest              ef9b5b747b7b        4 minutes ago       1.2GB
python              3.7.5               fbf9f709ca9f        3 weeks ago         917MB
mysql               latest              d435eee2caa5        3 weeks ago         456MB
ngrinder/agent      3.4                 f7594f30518f        3 years ago         175MB
```

<br>

Flask 앱 컨테이터 실행.

```
$ docker run -d --name flaboard -p 5000:5000 flaboard:0.1
```

<br>

`-d` 옵션을 빼면 로컬에서 `flask run`했을 때 나타나는 기본 로그까지 같이 출력할 수 있다.

```
$ docker run --name flaboard -p 5000:5000 flaboard:0.1
```

```
 * Serving Flask app "flaboard.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 165-887-641
```

<br>

역시 한번에 되면 불안하다. 컨테이너에 못 붙고 있다. docker도 일종의 외부 환경이기 때문에 EC2와 마찬가지로 IP를 허용해줘야 한다. 현재 IP 허용과 관련해서 경우의 수가 총 3개가 있다.

<br>

>1. *Dockerfile 파일의 CMD 항목에 `["run", "--host", "0.0.0.0"]`으로 명시*
>2. *app.py 파일에 `app.run(debug=False, host='0.0.0.0')` 메소드로 명시*
>3. *1번, 2번 둘 다 명시*

<br>

다다익선(?)이라고 3번은 일단 성공했다. 하나씩 지우면서 테스트를 진행해보도록 하겠다.
(이미지만 빨리 빌드되면 좋으련만.)

1번도 성공.

```
 * Serving Flask app "flaboard.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 908-270-774
```

<br>

2번은 실패.

```
 * Serving Flask app "flaboard.py" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 302-168-008
```

<br>

> *결론:  `app.run()` 메소드의  `host` 옵션과는 관계없이 `Dockerfile` 파일에 IP 허용 관련 커맨드까지 명시해줘야 가능하다.*

<br>

```dockerfile
# Dockerfile

FROM python:3.7.5

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["flask"]

CMD ["run", "--host", "0.0.0.0"]
```

<br>

D\docker가 `ENTRYPOINT`와 `CMD` 옵션을 조합하여 `flask run --host 0.0.0.0` 커맨드를 실행하게 된다.

<br>

> *ENTRYPOINT - 컨테이너가 수행될 때 변경되지 않을 커맨드를 정의*
>
> *CMD - 메인 커맨드 실행 시의 추가 옵션 인자 값을 정의*

<br>

### Push

많은 시간이 흘렀다. 만든 이미지를 이제 Docker Hub에 올리자!

```
$ docker login -u <Docker Hub ID>
```

<br>

혹시나 다른 개발자의 이미지와 이름이 충돌하지 않도록 태그를 달 것이다.

```
$ docker tag flaboard:0.1 yvvyoon/flaboard
$ docker images
```

```
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
flaboard            0.1                 534304e57b0b        15 minutes ago      1.2GB
yvvyoon/flaboard    0.1                 534304e57b0b        15 minutes ago      1.2GB
python              3.7.5               fbf9f709ca9f        3 weeks ago         917MB
mysql               latest              d435eee2caa5        3 weeks ago         456MB
ngrinder/agent      3.4                 f7594f30518f        3 years ago         175MB
```

<br>

동일한 `IMAGE ID`에 대해 다른 2개의 이미지 파일이 공존하는 것을 확인할 수 있다.

```
$ docker push yvvyoon/flaboard:0.1
```

```
The push refers to repository [docker.io/yvvyoon/flaboard]
5e16981b446e: Preparing
1992756b6c03: Preparing
86e3801e1814: Preparing
c9129ea28893: Preparing
7c3b00c0d411: Preparing
cecea5b3282e: Waiting
9437609235f0: Waiting
bee1c15bf7e8: Waiting
423d63eb4a27: Waiting
7f9bf938b053: Waiting
f2b4f0674ba3: Waiting
denied: requested access to the resource is denied
```

<br>

음... 아까 분명히 로그인했는데...

해결했다. 아까 이미지에 태그달 때 내가 원하는 이름 아무거나 붙이면 되는 줄 알았다. 내 맘대로 하는 게 아니라 Docker Hub의 username으로 지정해줘야 되는 거였다. :)

```
$ docker tag flaboard:0.1 yoon4480/flaboard
$ docker push yoon4480/flaboard:0.1
```

```
The push refers to repository [docker.io/yoon4480/flaboard]
5e16981b446e: Pushed
1992756b6c03: Pushed
86e3801e1814: Pushed
c9129ea28893: Pushed
7c3b00c0d411: Pushed
cecea5b3282e: Pushed
9437609235f0: Pushed
bee1c15bf7e8: Pushed
423d63eb4a27: Pushed
7f9bf938b053: Pushed
f2b4f0674ba3: Pushed
0.1: digest: sha256:30a4c76f7448c4c5c306a5a2ee1654e01a23bf54e68d39e22dbdc8ef0a600b2d size: 2641
```

<br>

<img width="949" alt="스크린샷 2019-12-19 오후 5 54 11" src="https://user-images.githubusercontent.com/12066892/71159288-b1140f80-2288-11ea-859d-67c37d3b638f.png">

<br>

### Pull

pull은 그 동안의 시행착오에 비해서 아주 아주 아주 쉽다. 태그를 포함한 이미지 이름이 이미 고유하기 때문에 pull할 때 별도의 설정을 해줄 필요가 없다. 로컬에서는 이미 돌고 있으니 번거롭게 컨테이너 내리지 말고 EC2에서 해보자.

<br>

> ***Ubuntu 18.04에 Docker 설치***
>
> ​	*https://phoenixnap.com/kb/how-to-install-docker-on-ubuntu-18-04*

<br>

```
$ docker pull yoon4480/flaboard:0.1
```

```0.1: Pulling from yoon4480/flaboard
16ea0e8c8879: Pull complete
50024b0106d5: Pull complete
ff95660c6937: Pull complete
9c7d0e5c0bc2: Pull complete
29c4fb388fdf: Pull complete
8659dae93050: Pull complete
1da0ab556051: Extracting [===================>                               ]  10.62MB/26.56MB
e92ae9350d4a: Download complete
c648cb7fc575: Download complete
34bdd5023a6c: Download complete
e2004367274a: Download complete
```

<br>

일부러 진행 중인 콘솔을 넣어봄. :)

```
Digest: sha256:30a4c76f7448c4c5c306a5a2ee1654e01a23bf54e68d39e22dbdc8ef0a600b2d
Status: Downloaded newer image for yoon4480/flaboard:0.1
```

<br>

EC2에도 잘 돌아간다. 이제 MySQL만 잘 뚫자. 끝.

