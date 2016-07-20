#coding=utf8
import threading
import multiprocessing
import signal
import time
import os, random
 
class Cmd(threading.Thread):

    def __init__(self,cmd):
        super(Cmd, self).__init__()
        self.cmd=cmd
         
    def run(self):
     
        print 'pre task cmd',self.cmd
        #time.sleep(80)
        #os.system("nohup sh /home/playcrab/release_tools/test.sh &")
        import subprocess
        p=subprocess.Popen(self.cmd,shell=True) 
        print 'task', self.cmd
