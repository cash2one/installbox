#coding=utf8

import multiprocessing
import signal
import time
import os, random
from cmd import Cmd
import threading



class Task(threading.Thread):
    def __init__(self,queue):
        super(Task, self).__init__()
        self.queue=queue
         
    def run(self):
        cmd = self.queue.get()
        print 'pre task cmd',cmd
        #time.sleep(80)
        t = Cmd(cmd)
        t.start()

        time.sleep(1)
