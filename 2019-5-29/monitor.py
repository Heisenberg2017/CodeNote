# ref: An introduction to Python Concurrency - David Beazley
from threading import Thread
from threading import RLock, Lock
import time


# 同一时间只有一条线程可以操作数据

class monitor(object):
    lock = RLock()

    # lock = Lock() # 死锁

    def foo(self, tid):
        with monitor.lock:
            print("%d in foo" % tid)
            time.sleep(5)
            self.ker(tid)

    def ker(self, tid):
        with monitor.lock:
            print("%d in ker" % tid)


m = monitor()


def task1(id):
    m.foo(id)


def task2(id):
    m.ker(id)


if __name__ == '__main__':
    t1 = Thread(target=task1, args=(1,))
    t2 = Thread(target=task2, args=(2,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()


