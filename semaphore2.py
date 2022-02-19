import httpx
import trio
from threading import Semaphore, Thread
import json
import time
import sys
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

# creating thread instance where count = 3
semaphore_obj = Semaphore(0)

# creating instance
def show(the_name):
    # calling acquire method
    semaphore_obj.acquire()
    for n in range(1):
        print('Javatpoint, ', end='')
        time.sleep(1/2)
        print(the_name)

        # calling release method  
        semaphore_obj.release(1)

    # creating multiple thread

# creating instance
def show2(the_name):
    # calling acquire method
    semaphore_obj.acquire()
    for n in range(1):
        print('Javatpoint 2, ', end='')
        time.sleep(1/2)
        print(the_name)

        # calling release method
        semaphore_obj.release(1)


thread_1 = Thread(target=show, args=('Thread 1',))
thread_2 = Thread(target=show, args=('Thread 2',))
thread_3 = Thread(target=show, args=('Thread 3',))
thread_4 = Thread(target=show2, args=('Thread 4',))
thread_5 = Thread(target=show2, args=('Thread 5',))
thread_6 = Thread(target=show2, args=('Thread 6',))

# calling the threads   
thread_1.start()
thread_2.start()
thread_3.start()
thread_4.start()
thread_5.start()
thread_6.start()
input('start')
semaphore_obj.release()
