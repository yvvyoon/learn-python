from multiprocessing import Process, Queue
import time


def summarize(id, start, end, result):
    mid_sum = 0
    start_time = time.time()

    for i in range(start, end):
        mid_sum += 1
        result.put(mid_sum)

    elapsed_time = time.time() - start_time

    print(f'Elapsed time: {elapsed_time}')

    return


if __name__ == '__main__':
    start, end = 0, 100000000
    result = Queue()
    process1 = Process(target=summarize, args=(1, start, end // 2, result))
    process2 = Process(target=summarize, args=(1, end // 2, end, result))

    process1.start()
    process2.start()
    process1.join()
    process2.join()

    result.put('STOP')
    mid_sum = 0

    while True:
        temp_result = result.get()
        print(f'temp_result: {temp_result}')

        if temp_result == 'STOP':
            break
        else:
            mid_sum += temp_result

    print(f'Result: {mid_sum}')
