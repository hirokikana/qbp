#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import time

script_path = os.path.abspath(os.path.dirname(__file__))
lib_path = '%s/../lib' % script_path
sys.path.append(lib_path)
import qbp

def list():
    pass

def add(command, execute_time = 0):
    if execute_time:
        execute_timestamp =  int(time.mktime(time.strptime(execute_time, '%Y/%m/%d-%H:%M:%S')))
        if execute_timestamp < int(time.time()):
            execute_timestamp = 0
    else:
        execute_timestamp = 0
    print execute_timestamp
    print command

    task_param = qbp.TaskParam({
            'command':command,
            'execute_time': execute_timestamp
            })
    redis_connection = qbp.RedisConnection('localhost', 6379, 'qbp_')

    if execute_timestamp == 0:
        if queue = qbp.Queue(redis_connection).enqueue(task_param):
            print 'add task success(queue)'
        else:
            print 'add task failed(queue)'
    else:
        if qbp.TaskPool(redis_connection).add(task_param):
            print 'add task success'
        else:
            print 'add task failed'
            

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "%s " % __file__
    else:
        operation = sys.argv[1]
        if operation == 'add':
            command = sys.argv[2]
            execute_time = None
            if len(sys.argv) > 3:
                execute_time = sys.argv[3]
            add(command,  execute_time)
        else:
            list()
    
