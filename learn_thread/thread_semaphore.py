import random
import threading
import time

semaphore = threading.Semaphore(value=0)

def consumer():
    print("consumer is waiting")
    semaphore.acquire()
    print("Consumer notify: consumerd item number {}".format(item))


def producer():
    global item
    time.sleep(10)
    item = random.randint(0, 1000)
    print("producer notify: produced item number {}".format(item))
    semaphore.release()


if __name__ == '__main__':
    # for i in range(5):
    #     t1 = threading.Thread(target=producer)
    #     t2 = threading.Thread(target=consumer)
    #     t1.start()
    #     t2.start()
    #     t1.join()
    #     t2.join()
    s = {1, 2, 3}
    print(1 in s)
    d = {'name': 'jason', 'age': 20}
    print(d["name"])
    print("program done")

    d = {'b': 1, 'c': 2, 'a': 10}
    d_sort_key = sorted(d.items(), key=lambda x: x[0])
    d_sort_value = sorted(d.items(), key=lambda x: x[1])
    print(d_sort_key)
    print(d_sort_value)
