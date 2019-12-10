## logging

파이썬에선 내장된 로깅 모듈을 이미 제공하고 있어서 단순 `import`하여 간편하게 사용할 수 있다.

<br>

### 중요도 수준

> *DEBUG:*
>
> - *상세한 정보. 보통 문제를 진단할 때만 필요*
>
> *INFO:*
>
> - *프로그램이 예상대로 잘 작동하는지에 대한 확인*
>
> *WARNING:*
>
> - *예상치 못한 일이 발생했거나 가까운 미래에 발생할 문제(예 - 디스크 공간 부족)에 대한 표시.*
> - *프로그램은 여전히 작동*
> - *로깅의 기본 수준은 **WARNING***
>
> *ERROR:*
>
> - *더욱 심각한 문제로 인해 프로그램 일부 기능이 수행되지 못함*
>
> *CRITICAL:*
>
> - *심각한 에러. 프로그램 자체가 계속 실행되지 않을 수 있음*

<br>

### 로그를 파일에 남기기

- logging-test.py

```python
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.debug('디버그~~')
logging.info('인포~~')
logging.warning('워닝~~')
```

`level` 속성에 로깅 수준을 `DEBUG`로 설정했기 때문에, 모든 메시지들이 출력된다.

로깅 수준을 설정하는 방법은 다양하다. 커맨드 라인에서 `--log` 옵션으로도 줄 수 있다.

```
--log=INFO
```

<br>

또, 특정 변수에**(예 - loglevel)**에 `--log`에 전달된 파라미터가 있다면

```python
getattr(logging, loglevel.upper())
```

이 방법도 가능하다.

<br>

- example.log

```
DEBUG:root:디버그~~
INFO:root:인포~~
WARNING:root:워닝~~
```

<br>

`filemode` 속성에 `w` 옵션을 주어 사용하면 로그 파일을 덮어씌우게 된다.

```
logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
```

<br>

### 복수의 모듈로 구성되어 있을 때의 로깅

방식은 복잡하지 않다. 하지만 어느 모듈로부터 온 로그인지는 이 코드를 통해서는 알 방법이 없다. 아마 `getLogger(name)` 메소드를 사용하는 것 같은데 이는 추후에 알아보자.

<br>

- myapp.py

```python
import logging

import mylib


def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('시작')
    mylib.do_something()
    logging.info('종료')


if __name__ == '__main__':
    main()
```

<br>

- mylib.py

```python
import logging


def do_something():
    logging.info('아무거나 하자!!')
```

<br>

- myapp.log

```
INFO:root:시작
INFO:root:아무거나 하자!!
INFO:root:종료
```

<br>

### 변수 데이터 로깅

로그 메시지에 특정 변수의 데이터도 포함시킬 수 있다. 이전 버전과의 호환성을 위해 `%` 연산자를 사용할 수도 있고, `str.format()`, `string.Template` 메소드도 사용이 가능하다.

```python
import logging

logging.warning('%s before you %s', 'Look', 'leap!')
```

<br>

### 메시지 포맷 변경

그 동안 기록해왔던 로그 메시지들을 보면 `레벨:root:메시지` 형식으로 표시된다. `format` 속성으로 이 포맷도 변경할 수 있다. 로그는 날짜/시간 없으면 노쓸모다. `%(asctime)s`와 `datefmt` 속성으로 날짜/시간까지 포함해서 출력해보자.

```python
logging.basicConfig(filename='example.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s]:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p')
```

```
DEBUG:디버그~~
INFO:인포~~
WARNING:워닝~~
2019-12-10 10:35:28,891 DEBUG:디버그~~
2019-12-10 10:35:28,891 INFO:인포~~
2019-12-10 10:35:28,891 WARNING:워닝~~
2019-12-10 10:35:55,520 [DEBUG]:디버그~~
2019-12-10 10:35:55,520 [INFO]:인포~~
2019-12-10 10:35:55,520 [WARNING]:워닝~~
2019/12/10 10:38:33 AM [DEBUG]:디버그~~
2019/12/10 10:38:33 AM [INFO]:인포~~
2019/12/10 10:38:33 AM [WARNING]:워닝~~
2019/12/10 AM 10:38:52 [DEBUG]:디버그~~
2019/12/10 AM 10:38:52 [INFO]:인포~~
2019/12/10 AM 10:38:52 [WARNING]:워닝~~
2019-12-10 10:45:48 AM [DEBUG]:디버그~~
2019-12-10 10:45:48 AM [INFO]:인포~~
2019-12-10 10:45:48 AM [WARNING]:워닝~~
```

<br>

## 모듈 방식으로 구성된 logging 라이브러리

logging 라이브러리는 아래와 같이 4개의 모듈로 구성된다.

> - *Logger: 프로그램 코드가 직접 사용하는 인터페이스를 노출*
> - *Handler: 로그 레코드를 적절한 목적지로 전달*
> - *Filter: 출력할 로그 레코드를 정밀하게 결정*
> - *Formatter: 로그 레코드의 형식 지정*

<br>

### Logger

`Logger` 객체는 주로 구성 및 메시지 전송을 핵심적으로 수행한다. `Logger.setLevel()` 메소드는 최소한의 심각도를 지정하는데 `DEBUG`가 가장 낮은 심각도이고, `INFO`로 설정하면 `DEBUG` 메시지는 무시한다. 

`Logger.addHandler()`와 `Logger.removeHandler()`는 핸들러의 추가/삭제, `Logger.addFilter()`와 `Logger.removeFilter()`는 필터의 추가/삭제의 역할을 수행한다.

<br>

### 로그 메시지 생성 메소드

`Logger.debug(), Logger.info(), Logger.warning(), Logger.error(), Logger.critical()`로 각 심각도 수준에 맞는 메소드를 사용한다.

`Logger.exception()` 메소드는 `Logger.error()`와의 다르게 스택 트레이스 덤프한다.

<br>

> *Stack trace(Stack traceback)*
>
> ​	*: 예외가 발생했을 때 프로그램이 실행 중에 호출한 메소드의 리스트. 디버깅이 필요한 코드의 위치를 알 수 있다.*

<br>

### 핸들러

프로그램은 일단 모든 로그 메시지를 로그 파일로 내보내고, `ERROR`와 그 이상의 로그 메시지는 표준 입출력, `CRITICAL` 메시지는 이메일로 보낼 수 있다. 핸들러는 이와 같은 시나리오처럼 특정 위치에 로그를 전달한다.

주로 `StreamHandler`와 `FileHandler`를 많이 사용되고, 핸들러 객체는 `setLevel()`, `setFormatter()`, `addFilter()`, `removeFilter()` 메소드들로 구성된다.

<br>

### 포매터

포매터 객체는 로그 메시지의 순서와 구조, 내용을 결정한다. 포매터 클래스를 `__init__` 메소드로 초기화할 수 있다.

<br>

> logging.Formatter.\__init__(fmt=None, datefmt=None, style='%')

<br>

`datefmt`가 지정되지 않으면 기본적으로 `%Y-%m-%d %H:%M:%S` 형식으로 출력된다.

`style` 속성은 `%`, `{`, `$` 중 하나를 사용하는데 아래와 같은 특성을 지닌다.

- %: `%(\<dictionary key>)` 스타일 문자열 치환
- {: `str.format()`로 치환
- $: `string.Template.substitute()`로 치환

<br>

### 기본적인 logger 사용

- loggging-test.py

```python
import logging

# 로거 생성
logger = logging.getLogger('simple_logger')
logger.setLevel(logging.DEBUG)

# 핸들러 생성
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# 포매터 생성
# %(name)s 속성은 로거의 이름을 출력
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 핸들러에 포매터 추가
console_handler.setFormatter(formatter)

# 로거에 핸들러 추가
logger.addHandler(console_handler)

logger.debug('debug 메시지')
logger.info('info 메시지')
logger.warning('warning 메시지')
logger.error('error 메시지')
logger.critical('critical 메시지')
```

```
2019-12-10 11:50:02,303 - simple_logger - DEBUG - debug 메시지
2019-12-10 11:50:02,303 - simple_logger - INFO - info 메시지
2019-12-10 11:50:02,303 - simple_logger - WARNING - warning 메시지
2019-12-10 11:50:02,303 - simple_logger - ERROR - error 메시지
2019-12-10 11:50:02,303 - simple_logger - CRITICAL - critical 메시지
```

<br>

### logging.config 사용

매번 로거를 설정해주지 않고 `.conf` 파일을 만들어서 관리할 수 있다.

- logging-test.py

```python
import logging
import logging.config


logging.config.fileConfig('logging.conf')

logger = logging.getLogger('simpleLogger')
logger.debug('debug 메시지')
logger.info('info 메시지')
logger.warning('warning 메시지')
logger.error('error 메시지')
logger.critical('critical 메시지')
```

<br>

- logging.conf

```q
[loggers]
keys=root, simpleLogger

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleLogger]
level=DEBUG
handlers=consoleHandler
qualname=simpleLogger
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=
```

<br>

앞의 코드에서 각 핸들러, 포매터에 대한 설정 로직이 빠진 것이 다르다. 이 설정 로직들이 모두 `conf` 파일에 모여 있다.

<br>

파이썬 3.1 버전부터 `NullHandler`라는 아무런 메시지를 출력하지 않는 핸들러를 지원한다.

```python
import logging


logging.getLogger('foo').addHandler(logging.NullHandler())
```

<br>

### 로깅이 처리되는 흐름 상기하기

로거가 특정 이벤트에 대해 로그를 남기기로 한다면 우선 로그 메시지는 `LogRecord` 클래스의 인스턴스로 인코딩된다. `Logger`의 `addHandler()` 메소드를 통해 핸들러 인스턴스가 추가되고, 이 핸들러에 의해 해당 로그 메시지가 정해진 목적지로 전달된다. 

<br>

>#### *여러* 핸들러
>
>*StreamHandler: 스트림(파일 스트림 객체)에 메시지를 전달*
>
>*FileHandler: 디스크 파일에 메시지 전달*
>
>*BaseRotatingHandler: `RotatingFileHandler`나 `TimedRotatingFileHandler`로 인스턴스화되어 로그 파일을 rotating함*
>
>*RotatingFileHandler: 최대 로그 파일 크기로 로그 파일 rotating*
>
>*TimedRotatingFileHandler: 일정한 시간 간격으로 로그 파일 rotating*
>
>*SocketHandler: TCP/IP 소켓에 메시지 전달*
>
>*DatagramHandler: UDP 소켓에 메시지 전달*
>
>*SMTPHandler: 이메일 주소로 메시지 전달*
>
>*SysLogHandler: Unix syslog 데몬(원격지도 가능)에 메시지 전달*
>
>*NTEventLogHandler: Windows NT/2000/XP 이벤트 로그에 메시지 전달*
>
>*MemoryHandler: 메모리에 있는 버퍼에 메시지 전달. 특정 기준이 충족될 때까지 flushing*
>
>*HTTPHandler: GET/POST를 사용하여 HTTP 서버에 메시지 전달*
>
>*WatchedFileHandler: 로깅하고 있는 파일 감시. 파일이 변경되면 종료하고 새로운 파일 이름을 사용하여 다시 열림.*
>
>*QueueHandler: 큐 또는 멀티프로세싱 모듈에 구현된 것과 같은 큐로 메시지 전달*
>
>*NullHandler: 에러 메시지에 아무 것도 나타나지 않음. Logging 라이브러리를 사용하긴 하는데 로깅을 구성하지 않을 때 발생하는 `No handlers could be found for logger XXX`라는 메시지를 숨기고자 할 때 사용.*

<br>

### 로깅 중의 예외 발생

로깅을 수행하면서 로깅 자체의 예외가 발생할 수 있다. 잘못된 로깅 구성, 네트워크 또는 기타 유사한 에러가 발생하여 로깅을 사용하는 프로그램을 갑작스럽게 종료시키지 않기 위해 `logging` 패키지는 그런 예외를 무효화하도록 설계되어 있다.

`SystemExit`, `KeyboardInterrupt` 예외는 `logging` 패키지에 의해 무효화되지 않는다. 