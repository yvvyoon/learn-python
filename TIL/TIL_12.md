## Logging

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
DEBUG:root:This message should go to the log file
INFO:root:So should this
WARNING:root:And this, too
```

<br>

