from threading import Thread
import time


def summarize(id, start, end, result):
    mid_sum = 0
    start_time = time.time()

    for i in range(start, end):
        mid_sum += 1
        result.append(mid_sum)

    duration = time.time() - start_time
    print(f'Duration of ID[{id}]: {duration}')

    return


if __name__ == '__main__':
    start, end = 0, 100000000
    result = list()
    thread1 = Thread(target=summarize, args=(1, start, end, result))

    thread1.start()
    thread1.join()


print(f'Result: {sum(result)}')
