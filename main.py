import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *
from config import *
import time

queue=Queue()
Spider(PROJECT_NAME,HOMEPAGE,DOMAIN_NAME)

def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t=threading.Thread(target=work)
        t.daemon=True
        t.start()

def work():
    while True:
        url=queue.get()
        Spider.crawl_page(threading.current_thread().name,url)
        queue.task_done()

def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

def crawl():
    queued_links=file_to_set(QUEUE_FILE)
    if len(queued_links)>0:
        print(str(len(queued_links))+ 'links in the queue')
        create_jobs()

start_time=time.time()
create_workers()
crawl()
end_time=time.time()

print("TIME TAKEN: ",end_time-start_time)