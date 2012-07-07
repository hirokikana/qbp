#!/usr/bin/env python
# -*- coding: utf-8 -*-
import redis
import time
import os

class RedisOperator:
    def __init__(self, command, connection, key_prefix, pipe = None):
        self.command = command
        self.connection = connection
        self.key_prefix = key_prefix
        self.pipe  = pipe
    
    def __call__(self, *redisargs):
        if len(redisargs) == 0:
            return eval('self.connection.%s()' % self.command)
        else:
            if redisargs[0].startswith(self.key_prefix):
                # prefixがすでについてたら付与しない
                add_key_prefix_args = redisargs
            else:
                # prefixを自動的に付与
                add_key_prefix_args = ('%s:%s' % (self.key_prefix, redisargs[0]),) + redisargs[1:]

            # コマンドを実行して返す
            if self.pipe:
                return eval('self.pipe.%s(*add_key_prefix_args)' % self.command)
            else:
                return eval('self.connection.%s(*add_key_prefix_args)' % self.command)
        
class RedisConnection:
    def __init__(self, host='localhost', port=6379, key_prefix='qbp_DEFAULT_PREFIX_'):
        self.connection = redis.Redis(host=host,port=port)
        self.key_prefix = key_prefix
        # pipeline
        self.pipe = None

    def begin_transaction(self):
        if self.pipe == None:
            self.pipe = RedisOperator('pipeline', self.connection, self.key_prefix, self.pipe)();
            return True
        else:
            return False

    def commit_transaction(self):
        self.pipe.execute()
        self.pipe = None
        return True

    def __nonzero__(self):
        return True
    
    def __getattr__(self, command):
        return RedisOperator(command, self.connection, self.key_prefix, self.pipe)
    
class Queue:
    def __init__(self, connection = None):
        if connection:
            self.connection = connection
        else:
            self.connection = RedisConnection();

    # タスクを追加
    def enqueue(self, param):
        if not isinstance(param , TaskParam):
            raise ValueError('enqueue argument require TaskParam')

        taskinfo = TaskInfo()
        if not param.get_id():
            param = TaskInfo().add(param)
        task_id = int(param.get_id())
        
        result = self.connection.lpush('queue', task_id)
        if not result == False:
            return param
        else:
            return 0
        

    # タスクを取得(brpopで待つだけ)
    def dequeue(self):
        task_id = self.connection.brpop('queue')
        result = TaskInfo().get(task_id[1])
        return result

    def count(self):
        result = self.connection.llen('queue')
        return result

    def truncate(self):
        return self.connection.delete('queue')

class TaskPool:
    def __init__(self, connection = None):
        if connection:
            self.connection = connection
        else:
            self.connection = RedisConnection()

    # taskpoolにタスクIDを追加
    def add(self, task_param):
        if not isinstance(task_param,TaskParam):
            return False

        # idが指定されていないときはtaskinfoに追加
        if not task_param.get_id():
            task_info = TaskInfo()
            task_info.add(task_param)
        
        result = self.connection.zadd('taskpool', task_param.get_id(), task_param.get_execute_time())
        if isinstance(result, int):
            return True
        else:
            return False

    # 実行時間をすぎているタスクを取得
    def get(self):
        self.connection.watch('taskpool');
        result = self.connection.zrangebyscore('taskpool', 0, time.time())
        if len(result):
            task_id = result[0]
            self.connection.begin_transaction()
            self.connection.zrem('taskpool', task_id)
            self.connection.commit_transaction()
            return int(task_id)
        else:
            return False

    # 現在のタスク数を返す
    def count(self):
        count = self.connection.zcard('taskpool')
        return count

    # タスクをiterationを使って取得
    def task(self):
        while True:
            result = self.get()
            if result:
                yield result
            else:
                break
            

    # 指定したタスクを削除
    def delete(self, task_id):
        return self.connection.zrem('taskpool', task_id)

    # 全部のタスクをクリア
    def truncate(self):
        task_id_list = self.connection.zrange('taskpool', 0, -1)
        for task_id in task_id_list:
            self.delete(task_id)

class TaskInfo:
    def __init__(self, connection = None):
        if connection:
            self.connection = connection
        else:
            self.connection = RedisConnection()

    def __get_id(self):
        task_id = self.connection.incr('taskinfo:taskid')
        return task_id

    def __set(self, param_dict):
        key = 'taskinfo:%s' % param_dict['id']
        for dict_key in param_dict.keys():
            self.connection.hset(key, dict_key, param_dict[dict_key])
        return TaskParam(param_dict)

    def set(self, task_param):
        if not isinstance(task_param, TaskParam):
            raise ValueError('argument require TaskParam')
        task_id = int(task_param.get_id())
        param_dict = task_param.as_dict()
        return self.__set(param_dict)
        
    
    def add(self, task_param):
        if not isinstance(task_param, TaskParam):
            raise ValueError('argument require TaskParam')
        param_dict = task_param.as_dict()

        param_dict['id'] = self.__get_id()
        return self.__set(param_dict)

    def get(self, task_id):
        key = 'taskinfo:%s' % int(task_id)
        result = self.connection.hgetall(key)
        if result:
            return TaskParam(result)
        else:
            return None

    def delete(self, task_id):
        key = 'taskinfo:%s' % int(task_id)
        return self.connection.delete(key)

    def truncate(self):
        # idとタスク情報を削除
        used_keys = self.connection.keys('taskinfo:*')
        for key in used_keys:
            self.connection.delete(key)
        
class TaskParam:
    def __init__(self, param = {}):
        self.private = {}
        self.private['id'] = None
        self.private['execute_time'] = 0
        self.private['stdout'] = ''
        self.private['stderr'] = ''
        self.private['command'] = ''

        if param.has_key('id'):
            self.set_id(param['id'])
        if param.has_key('execute_time'):
            self.set_execute_time(param['execute_time'])
        if param.has_key('stdout'):
            self.set_stdout(param['stdout'])
        if param.has_key('stderr'):
            self.set_stderr(param['stderr'])
        if param.has_key('command'):
            self.set_command(param['command'])

    def get_id(self):
        return self.private['id']

    def get_command(self):
        return self.private['command']

    def get_stdout(self):
        return self.private['stdout']

    def get_stderr(self):
        return self.private['stderr']

    def get_execute_time(self):
        return self.private['execute_time']

    def set_id(self, task_id):
        self.private['id'] = int(task_id)

    def set_execute_time(self, execute_time):
        self.private['execute_time'] = int(execute_time)

    def set_stdout(self, msg):
        self.private['stdout'] = msg

    def set_stderr(self, msg):
        self.private['stderr'] = msg

    def set_command(self, command):
        self.private['command'] = command
        
    def as_dict(self):
        return self.private

import logging
class Logger:
    def get_logger(self, log_name):
        script_path = os.path.abspath(os.path.dirname(__file__))
        log_path = '%s/../log/%s.log' % (script_path, log_name)

        console_log = logging.StreamHandler()
        console_log.setLevel(logging.DEBUG)
        console_log.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))

        file_log = logging.FileHandler(filename=log_path)
        file_log.setLevel(logging.DEBUG)
        file_log.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
        
        logger = logging.getLogger()

        logger.addHandler(console_log)
        logger.addHandler(file_log)
        logger.setLevel(logging.DEBUG) # これは伝播させるためにDEBUG固定

        return logger

        

    
