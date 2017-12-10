#!/usr/bin/env python
# -*- encoding: utf-8  -*-

""" 
@version: v1.0 
@author: jayzhen 
@license: Apache Licence  
@contact: jayzhen_testing@163.com 
@site: http://blog.csdn.net/u013948858 
@software: PyCharm 
@time: 2017/7/27 23:29 
"""
import string

from app.api_v1_2.controller.core.adb import AndroidUtils
from app.api_v1_2.controller.device_cursor import Device


class TopCpuMemParser(object):
    def __init__(self):
        # 打开待测应用，运行脚本，默认times为30次（可自己手动修改次数），获取该应用cpu、memory占用率的曲线图，图表保存至chart目录下
        self.utils = AndroidUtils()

    # 获取cpu、mem占用
    def top(self, sno, times, pkg_name):
        cpu = []
        mem = []
        if times is None or times == "":
            # top次数
            times = 30
        else:
            times = string.atoi(times)
            if times < 15 and times > 0:
                times = 20
        di = Device()
        if pkg_name is None or pkg_name == "" or not di.is_installed_package(sno, pkg_name):
            pkg_name = self.utils.current_package_name(sno)
        elif di.is_running_package(sno, pkg_name):
            # 设备当前运行应用的包名
            pkg_name = pkg_name
        else:
            return None
        top_info = self.utils.shell(sno, "top -n %s | findstr %s$" % (str(times), pkg_name)).stdout.readlines()
    #  PID PR CPU% S #THR VSS RSS PCY UID Name
        for info in top_info:
            # temp_list = del_space(info)
            temp_list = info.split()
            cpu.append(temp_list[2])
            mem.append(temp_list[6])
        return cpu, mem, pkg_name, times

