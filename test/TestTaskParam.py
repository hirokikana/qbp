#!/usr/bin/env python
# -*- coding:utf-8 -*-
from nose.tools import *
import sys
sys.path.append('../lib')
import qbp

class TestTaskParam():
    def test_create_instance(self):
        # インスタンス化されているか
        taskparam = qbp.TaskParam()
        ok_(isinstance(taskparam, qbp.TaskParam))

        # デフォルト値の確認
        eq_(taskparam.get_id(), None)
        eq_(taskparam.get_command(), '')
        eq_(taskparam.get_stdout(), '')
        eq_(taskparam.get_stderr(), '')
        eq_(taskparam.get_execute_time(), 0)

        # param指定のテスト
        param = {}
        param['id'] = 1
        param['execute_time'] = 200
        param['stdout'] = "hogehoge\nhogehoge"
        param['stderr'] = "hogehoge\nerr"
        param['command'] = 'cat /etc/passwd'
        taskparam = qbp.TaskParam(param)
        ok_(isinstance(taskparam, qbp.TaskParam))
        eq_(taskparam.get_id(), 1)
        eq_(taskparam.get_command(), 'cat /etc/passwd')
        eq_(taskparam.get_stdout(), "hogehoge\nhogehoge")
        eq_(taskparam.get_stderr(), "hogehoge\nerr")
        eq_(taskparam.get_execute_time(), 200)

    def test_id(self):
        taskparam = qbp.TaskParam()
        eq_(taskparam.get_id(), None)

        taskparam.set_id(200)
        eq_(taskparam.get_id(), 200)

        taskparam.set_id('201')
        eq_(taskparam.get_id(), 201)

        assert_raises(ValueError, taskparam.set_id, 'hoge')

        taskparam = qbp.TaskParam({'id':202})
        eq_(taskparam.get_id(), 202)

        taskparam = qbp.TaskParam({'id':'203'})
        eq_(taskparam.get_id(), 203)

    def test_command(self):
        taskparam = qbp.TaskParam()
        eq_(taskparam.get_command(), '')

        taskparam.set_command('/hoge')
        eq_(taskparam.get_command(), '/hoge')

    def test_stdout(self):
        taskparam = qbp.TaskParam()
        eq_(taskparam.get_stdout(), '')

        taskparam.set_stdout("hogehogehogheoge\nhogehoge");
        eq_(taskparam.get_stdout(), "hogehogehogheoge\nhogehoge")

    def test_stderr(self):
        taskparam = qbp.TaskParam()
        eq_(taskparam.get_stderr(), '')

        taskparam.set_stderr("hogehoge\nhoge")
        eq_(taskparam.get_stderr(), "hogehoge\nhoge")

    def test_execute_time(self):
        taskparam = qbp.TaskParam()
        eq_(taskparam.get_execute_time(), 0)

        taskparam.set_execute_time(50)
        eq_(taskparam.get_execute_time(), 50)
        
        taskparam.set_execute_time(100.15)
        eq_(taskparam.get_execute_time(), 100)

        assert_raises(ValueError, taskparam.set_execute_time, 'hogehoge')

    def test_as_dict(self):
        taskparam = qbp.TaskParam()
        taskparam.set_id(200)
        eq_(taskparam.get_id(), 200)
        result = taskparam.as_dict()
        ok_(isinstance(result, dict))
        eq_(result['id'], 200)
            
        
        
        
    
