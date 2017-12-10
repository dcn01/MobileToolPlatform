#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: status_enum
@time: 2017/11/22  11:30
"""

# import enum


runtime_attribute = {
    'unconnect': (10008, "Check if your device is connected properly"),
    'curt_pkg': (10001, "got mobile current running package name happend error"),  # 当前运行的app
    'curt_act': (10002, "got mobile current running activity happend error"),  # 当前app所在的activity
    'app_permission': (10003, "got mobile current app system permission happend error"),  # 当前app的应用权限
    'screen_status': (10004, "got mobile current screen_status happend error"),  # 当前是否锁屏10:锁黑、11：锁亮、01：开亮、00：开黑
    'wifi_status': (10005, "got mobile current wifi status happend error"),  # 当前wifi状态
    'curt_cpu': (10006, "got mobile current cpu info happend error"),  # 当前使用的cpu
    'curt_mem': (10007, "got mobile current mem info happend error"),  # 当前使用的mem
    'curt_battery': (10007, "got mobile current battery info happend error"),  # 当前的电量
}