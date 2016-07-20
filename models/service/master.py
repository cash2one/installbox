#coding=utf8

import threading
import multiprocessing
import signal
import time
import os, random
from task import Task  


class NoDaemonProcess(multiprocessing.Process):
    # make 'daemon' attribute always return False
    def _get_daemon(self):
        return False
    def _set_daemon(self, value):
        pass
    daemon = property(_get_daemon, _set_daemon)

 
class Master(threading.Thread):

    queue = multiprocessing.Queue()

    def __init__(self,cmd):
        super(Master, self).__init__()
        self.cmd = cmd     
         
    def run(self):
        Master.queue.put(self.cmd)
        t=Task(Master.queue)
        t.daemon=True
        t.start()
        time.sleep(3)
        #t.terminate()
        #import signal
        #os.kill(t.pid,signal.SIGKILL)
        #t.join()
