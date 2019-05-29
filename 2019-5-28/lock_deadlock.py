import threading
from contextlib import contextmanager

# 竞争
count = 0


def counter1(thread_id):  # count <= 2000000
    global count
    for _ in range(1000000):
        count += 1


def counter2(lock, thread_id):  # count == 2000000
    global count
    for _ in range(1000000):
        lock.acquire()
        count += 1
        lock.release()


# 加锁/守护线程

def add_lock():
    lock = threading.Lock()
    for thread_id in range(2):
        # daemon=True 守护线程与主线程共存亡, count未完全计算完毕,进程关闭
        # daemon=False 主线程输出count后结束, count完全计算完毕后,进程关闭
        x = threading.Thread(target=counter1, args=(lock, thread_id),
                             daemon=True)
        x.start()
        x.join()  # 主线程会等待join的线程/守护线程执行完毕后再继续执行
    print(count)


# 同时获取两次锁, 死锁

def dead_lock1():
    l = threading.Lock()
    print("before first acquire")
    l.acquire()
    print("before second acquire")
    l.acquire()
    print("acquired lock twice")


def task1(thread_id, l1, l2):
    l1.acquire()
    l2.acquire()


def task2(thread_id, l1, l2):
    l2.acquire()
    l1.acquire()


# 线程1获取l1后等待线程2释放l2,线程2获取l2后等待线程1释放l1, 造成死锁

def dead_lock2():
    l1 = threading.Lock()
    l2 = threading.Lock()
    for thread_id in range(2):
        # daemon=True 守护线程与主线程共存亡, count未完全计算完毕,进程关闭
        # daemon=False 主线程输出count后结束, count完全计算完毕后,进程关闭
        x = threading.Thread(target=task1 if thread_id == 0 else task2,
                             args=(thread_id, l1, l2), daemon=True)
        x.start()
        x.join()


# 解决死锁,只允许按照lock升序获取锁


# Thread-local state to stored information on locks already acquired
_local = threading.local()


@contextmanager
def acquire(*locks):
    # Sort locks by object identifier
    locks = sorted(locks, key=lambda x: id(x))

    # Make sure lock order of previously acquired locks is not violated
    acquired = getattr(_local, 'acquired', [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('Lock Order Violation')

    # Acquire all of the locks
    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        # Release locks in reverse order of acquisition
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]


x_lock = threading.Lock()
y_lock = threading.Lock()


# 死锁问题解决


# def thread_1():
#     while True:
#         with acquire(x_lock, y_lock):
#             print('Thread-1')
#
#
# def thread_2():
#     while True:
#         with acquire(y_lock, x_lock):
#             print('Thread-2')
#
#
# def non_deadlock():
#     t1 = threading.Thread(target=thread_1)
#     t1.daemon = True
#     t1.start()
#
#     t2 = threading.Thread(target=thread_2)
#     t2.daemon = True
#     t2.start()


def thread_1():
    while True:
        with acquire(x_lock):
            with acquire(y_lock):
                print('Thread-1')


def thread_2():
    while True:
        with acquire(y_lock):
            with acquire(x_lock):
                print('Thread-2')


def runtime_err():
    t1 = threading.Thread(target=thread_1)
    t1.daemon = True

    t2 = threading.Thread(target=thread_2)
    t2.daemon = True
    t2.start()
    t1.start()
    t1.join()
    t2.join()


if __name__ == '__main__':
    # add_lock()
    # dead_lock1()
    # dead_lock2()
    # non_deadlock()
    runtime_err()
