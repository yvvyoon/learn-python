import logging
import logging.config


logging.config.fileConfig('logging.conf')

# 로거 생성
logger = logging.getLogger('simpleLogger')
# logger.setLevel(logging.DEBUG)

# 핸들러 생성
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)

# 포매터 생성
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 핸들러에 포매터 추가
# console_handler.setFormatter(formatter)

# 로거에 핸들러 추가
# logger.addHandler(console_handler)

logger.debug('debug 메시지')
logger.info('info 메시지')
logger.warning('warning 메시지')
logger.error('error 메시지')
logger.critical('critical 메시지')