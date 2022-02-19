# ConnectionPoolSingleton.py
from threading import Lock, Semaphore, Thread, Event
import time
from MyConnection import *
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

class ConnectionPoolSingleton(object):
    _instance = None
    _lock = Lock()
    _lock_pool = Lock()
    _max_connections = 2
    semaphore_obj = Semaphore(_max_connections)

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def get_instance(cls):
        if cls._instance:
            return cls._instance
        with cls._lock:
            if cls._instance is None: #t1 + t2
                cls._instance = cls.__new__(cls)
                cls._instance.connections = [MyConnection(i + 1) for i in range(cls._max_connections)]
                cls._instance.free_conn_event = Event()
                cls._instance.free_conn_event.set()
            return cls._instance

    def get_free_count(self):
        return len(self.connections)

    def get_max_possible_connections(self):
        return ConnectionPoolSingleton._max_connections

    def get_connection(self):
        # will return a connection and remove it from the list
        # return self.connections ...
        # lock
        logging.debug('try to get connection')
        ConnectionPoolSingleton.semaphore_obj.acquire()
        with self._lock_pool:
            conn = self.connections.pop(0)
            logging.debug(f'taking connection {conn.number}')
            return conn

    def return_connection(self, conn):
        self.connections.append(conn)  # list python is thread safe
        ConnectionPoolSingleton.semaphore_obj.release()
        
        
# main.py
# main.py
from ConnectionPoolSingleton import ConnectionPoolSingleton
from MyConnection import MyConnection
from threading import Semaphore, Thread
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

pool = ConnectionPoolSingleton.get_instance()

conn1 = pool.get_connection()
#logging.debug(conn1)
conn2 = pool.get_connection()
#logging.debug(conn2)

def delay_return(t, conn):
    time.sleep(t)
    pool.return_connection(conn)

def delay_take(t):
    time.sleep(t)
    pool.get_connection()

Thread(name='thread-3', target=delay_take,
                          args=(2,)).start()

Thread(name='thread-1', target=delay_return,
                          args=(5,conn2)).start()

conn3 = pool.get_connection()
#logging.debug(conn3)

Thread(name='thread-2', target=delay_return,
                          args=(3,conn2)).start()
Thread(name='thread-4', target=delay_return,
                          args=(5,MyConnection(20))).start()
conn4 = pool.get_connection()
#logging.debug(conn4)
