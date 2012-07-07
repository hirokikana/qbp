#!/usrb/bin/env python
# -*- coding:utf-8 -*-
from nose.tools import *
import sys
sys.path.append('../lib')
import qbp

class TestTaskPool():
    def setup(self):
        self.pool = qbp.TaskPool()

    def teardown(self):
        self.pool.truncate()

    def test_instance(self):
        ok_(isinstance(self.pool, qbp.TaskPool))

    def test_add(self):
        param = qbp.TaskParam({'id':1})
        result = self.pool.add(param)
        eq_(result, True)

        # 異常系
        for param in [{}, '', (), []]:
            result = self.pool.add(param)
            eq_(result, False)

    def test_count(self):
        param = qbp.TaskParam({'id':1})
        result = self.pool.add(param)
        eq_(result, True)
        eq_(self.pool.count(), 1)

        param = qbp.TaskParam({'id':2})
        result = self.pool.add(param)
        eq_(result, True)
        eq_(self.pool.count(), 2)
    
    def test_get(self):
        param = qbp.TaskParam({'id':1})
        result = self.pool.add(param)
        eq_(result, True)
        task_id = self.pool.get()
        eq_(task_id, 1)
        
        task_id = self.pool.get()
        eq_(task_id, False)

    def test_iteration(self):
        param = qbp.TaskParam({'id':1})
        result = self.pool.add(param)
        eq_(result, True)
        for task_id in self.pool.task():
            eq_(task_id, 1)
        
