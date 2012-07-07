#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nose.tools import *
import sys
sys.path.append('../lib')
import qbp

class TestQueue():
    def setup(self):
        self.queue = qbp.Queue();

    def teardown(self):
        self.queue.truncate();
        qbp.TaskInfo().truncate()

    def test_truncate(self):
        param = qbp.TaskParam()
        result = self.queue.enqueue(param)

        eq_(self.queue.count(), 1)
        eq_(True, self.queue.truncate())
        eq_(self.queue.count(), 0)
        eq_(False, self.queue.truncate())
        
    
    def test_create_instance(self):
        ok_(isinstance(self.queue, qbp.Queue))
        
    def test_enqueue(self):
        param = qbp.TaskParam()
        task_param = self.queue.enqueue(param)
        ok_(isinstance(task_param, qbp.TaskParam))

        # task param以外
        for param in [None, '', 'hoge', 1]:
            assert_raises(ValueError, self.queue.enqueue, param)

        # id指定
        task_info = qbp.TaskInfo()
        param = qbp.TaskParam({'id':10})
        task_info.set(param)
        result = self.queue.enqueue(param)
        eq_(result.get_id(), 10)


    def test_dequeue(self):
        param = qbp.TaskParam()
        result = self.queue.enqueue(param)
        param = qbp.TaskParam()
        result = self.queue.enqueue(param)

        result = self.queue.dequeue()
        ok_(isinstance(result, qbp.TaskParam))
        eq_(result.get_id(), 1);

        result = self.queue.dequeue()
        eq_(result.get_id(), 2);

        # id付き(先に別途taskinfoに情報を入れていることが前提)
        #  本来であればtaskinfoにaddを勝手にする
        task_info = qbp.TaskInfo()
        param = qbp.TaskParam({'id':10})
        task_info.set(param)
        self.queue.enqueue(param)
        result = self.queue.dequeue()
        eq_(result.get_id(), 10)

    def test_count(self):
        param = qbp.TaskParam()
        result = self.queue.enqueue(param)
        param = qbp.TaskParam()
        result = self.queue.enqueue(param)

        eq_(self.queue.count(), 2)


    
