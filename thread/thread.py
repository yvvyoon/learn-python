from threading import Thread
import time


def summarize(id, start, end, result):
    mid_sum = 0
    start_time = time.time()

    for i in range(start, end):
        mid_sum += 1
        result.append(mid_sum)

    elapsed_time = time.time() - start_time
    print(f'Elapsed time of ID[{id}]: {elapsed_time}')

    return


if __name__ == '__main__':
    start, end = 0, 100000000
    result = list()

    thread1 = Thread(target=summarize, args=(1, start, end // 2, result))
    thread2 = Thread(target=summarize, args=(2, end // 2, end, result))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()


print(f'Result: {sum(result)}')
