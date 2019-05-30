import os
import time
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

from queue import Queue

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


def add_url(url, url_queue, html_queue, item_queue):
    logging.info(f"{url} > add")
    url_queue.put(f"{url} > add")


def fetch_page(url_queue, html_queue, item_queue):
    while True:
        item = url_queue.get()
        logging.info(f"{item} > fetch")
        time.sleep(1)
        html_queue.put(f"html <{os.urandom(5).hex()}>")


def parse_html(url_queue, html_queue, item_queue):
    while True:
        html = html_queue.get()
        logging.info(f"{html} > parse")
        time.sleep(0.5)
        for _ in range(3):
            add_url(f"{html} > parse > {os.urandom(5).hex()}", url_queue,
                    html_queue, item_queue)
        for _ in range(10):
            item_queue.put(f"item <{os.urandom(5).hex()}>")


def save_data(url_queue, html_queue, item_queue):
    while True:
        item = item_queue.get()
        logging.info(f"{item} > save data")
        time.sleep(0.2)


if __name__ == '__main__':
    url_queue = Queue(-1)
    html_queue = Queue(-1)
    item_queue = Queue(-1)
    url_template = "url {} "
    url_queue.put(url_template.format(os.urandom(5).hex()))
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(fetch_page, url_queue, html_queue, item_queue)
        executor.submit(parse_html, url_queue, html_queue, item_queue)
        executor.submit(save_data, url_queue, html_queue, item_queue)
