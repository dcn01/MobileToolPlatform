#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: runtime_infos.py
@time: 2017/11/7 21:27
"""


class Runtime(object):

    def __init__(self):
        self.curt_pkg = None  # 当前运行的app
        self.curt_act = None  # 当前app所在的activity
        self.app_permission = None  # 当前app的应用权限
        self.screen_status = None  # 当前是否锁屏10:锁黑、11：锁亮、01：开亮、00：开黑
        self.wifi_status = None   # 当前wifi状态
        self.curt_cpu = None   # 当前使用的cpu
        self.curt_mem = None   # 当前使用的mem
        self.curt_battery = None   # 当前的电量
