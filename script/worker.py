#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import os
import time
import subprocess

script_path = os.path.abspath(os.path.dirname(__file__))
lib_path = '%s/../lib' % script_path
sys.path.append(lib_path)
import qbp

log = qbp.Logger().get_logger('worker')

def mainloop():
    redis_connection = qbp.RedisConnection('localhost', 6379, 'qbp_')
    queue = qbp.Queue(redis_connection)

    while True:
        task = queue.dequeue()
        command = '%s/command_runner.py %s 2>&1 >/dev/null &' % (script_path, task.get_id())
        subprocess.call(command, shell=True)
        log.info('task exec: id=%s, command=%s' % (task.get_id(), task.get_command()))
        

if __name__ == '__main__':
    log.info('start worker')
    mainloop()
    
