#!/usr/bin/env python
# -*- coding:utf-8 -*-
from nose.tools import *
import sys
sys.path.append('../lib')
import qbp

class TestTaskInfo():
    def setup(self):
        self.taskinfo = qbp.TaskInfo()

    def teardown(self):
        self.taskinfo.truncate()
        
    def test_add(self):
        # 追加してIDが帰ってくることを確認
        task_param = qbp.TaskParam()
        result = self.taskinfo.add(task_param)
        ok_(isinstance(result, qbp.TaskParam))
        eq_(result.get_id(), 1)

    def test_get(self):
        task_param = qbp.TaskParam({'execute_time':200})
        result = self.taskinfo.add(task_param)
        eq_(result.get_id(), 1)
        task_param = qbp.TaskParam({'execute_time':100})
        result = self.taskinfo.add(task_param)
        eq_(result.get_id(), 2)

        result = self.taskinfo.get(1)
        eq_(result.get_id(), 1)
        eq_(result.get_execute_time(), 200)

        # 引数が不正
        assert_raises(ValueError, self.taskinfo.get, 'hogehoge')
        
    def test_delete(self):
        task_param = qbp.TaskParam({'execute_time':200})
        result = self.taskinfo.add(task_param)
        eq_(result.get_id(), 1)
        self.taskinfo.delete(1)
        # 削除後に取得できないことを確認
        result = self.taskinfo.get(1)
        eq_(result, None)
        
        # 引数が不正
        assert_raises(ValueError, self.taskinfo.get, 'hogehoge')
        
    def test_truncate(self):
        task_param = qbp.TaskParam({'execute_time':200})
        result = self.taskinfo.add(task_param)
        eq_(result.get_id(), 1)
        self.taskinfo.truncate()
        result = self.taskinfo.get(1)
        eq_(result, None)
        
        
    
