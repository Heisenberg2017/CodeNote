# coding = utf-8
import time
import logging
import threading
from concurrent.futures import ThreadPoolExecutor
import random
from queue import Queue

SENTINEL = object()

logging.basicConfig(
    format="%(asctime)s: %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S")
queue = Queue()


class Pipeline:

    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def get_message(self, name):
        logging.debug(f"{name}:about to acquire getlock")
        self.consumer_lock.acquire()
        logging.debug(f"{name}:have getlock")
        message = self.message
        logging.debug(f"{name}:about to release setlock")
        self.producer_lock.release()
        logging.debug(f"{name}:setlock released")
        return message

    def set_message(self, message, name):
        logging.debug(f"{name}:about to acquire setlock")
        self.producer_lock.acquire()
        logging.debug(f"{name}:have setlock")
        self.message = message
        logging.debug(f"{name}:about to release getlock")
        self.consumer_lock.release()
        logging.debug(f"{name}:get lock released")


def producer(pipeline):
    for index in range(10):
        message = random.randint(1, 101)
        logging.info(f"Producer got message {message}")
        pipeline.set_message(message, "Producer")

    pipeline.set_message(SENTINEL, "Producer")


def consumer(pipeline):
    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info(f"Consumer storing message {message}")


if __name__ == '__main__':
    pipeline = Pipeline()
    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)
