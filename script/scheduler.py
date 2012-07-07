#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
import os
import time

script_path = os.path.abspath(os.path.dirname(__file__))
lib_path = '%s/../lib' % script_path
config_path = '%s/../config/' % script_path
sys.path.append('%s/../lib' % script_path)
import qbp


log = qbp.Logger().get_logger('scheduler')

def mainloop(timing):
    redis_connection = qbp.RedisConnection('localhost', 6379, 'qbp_')
    task_pool = qbp.TaskPool(redis_connection)
    task_info = qbp.TaskInfo()
    queue = qbp.Queue(redis_connection)
    
    # 定期的に監視
    while True:
        for task_id in task_pool.task():
            if task_id:
                param = task_info.get(task_id)
                queue.enqueue(param)
                log.info('push queue: id=%s' % task_id)
                
        if int(time.time()) % 60 == 0:
            log.info('taskpool in %s task' % task_pool.count())
        time.sleep(timing)

if __name__ == '__main__':
    log.info('start scheduler')
    timing = 1
    mainloop(timing)
    

