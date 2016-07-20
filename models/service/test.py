#coding=utf8

import multiprocessing
import signal
import time
import os, random
from master import Master 
 
class Test(multiprocessing.Process):


    def __init__(self,cmd):
        super(Test, self).__init__()
        self.cmd = cmd 
         
    def run(self):
        print "ssss"
        t=Master(self.cmd)
        #t.daemon=True
        t.start()
        time.sleep(0.5)
        #t.terminate()

#t = Test('ls')
#t.start()
#time.sleep(2)
#t.terminate()
