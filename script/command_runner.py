#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess 

script_path = os.path.abspath(os.path.dirname(__file__))
lib_path = '%s/../lib' % script_path
sys.path.append('%s/../lib' % script_path)
import qbp

task_id = sys.argv[1]
task_info = qbp.TaskInfo()
param = task_info.get(task_id)
if param:
    command = (param.get_command())
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_str = ''
    stderr_str = ''
    for line in process.stdout.read():
        stdout_str += line
    for line in process.stderr.read():
        stderr_str += line

    # 標準出力と標準エラー出力を保存
    param_dict = param.as_dict()
    param_dict['stderr'] = stderr_str
    param_dict['stdout'] = stdout_str
    task_param = qbp.TaskParam(param_dict)
    task_info.set(task_param)
    
    print command
    print stdout_str
    print '------------------------'
    print stderr_str
    
