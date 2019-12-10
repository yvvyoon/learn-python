import logging

import mylib


def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logging.info('시작')
    mylib.do_something()
    logging.info('종료')


if __name__ == '__main__':
    main()
