import logging
import queue
import random
import threading
import time


def producer(queue, event):
    """Pretend we're getting a number from the network."""
    while not event.is_set():
        message = random.randint(1, 101)
        logging.info("Producer got message: %s", message)
        queue.put(message)

    logging.info("Producer received event. Exiting")


def consumer(queue, event):
    """Pretend we're saving a number in the database."""
    while not event.is_set() or not queue.empty():
        message = queue.get()
        logging.info(
            "Consumer storing message: %s (size=%d)", message, queue.qsize()
        )

    logging.info("Consumer received event. Exiting")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()

    # 线程池实现
    # with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    #     executor.submit(producer, pipeline, event)
    #     executor.submit(consumer, pipeline, event)
    #
    # 线程实现
    producer_tasks = [
        threading.Thread(target=producer, args=(pipeline, event)) for i in
        range(3)]
    consumer_tasks = [
        threading.Thread(target=consumer, args=(pipeline, event)) for i in
        range(3)]
    [p.start() for p in producer_tasks]
    [c.start() for c in consumer_tasks]

    time.sleep(0.1)
    logging.info("Main: about to set event")
    event.set()
