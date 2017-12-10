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
import threading
import json
import os
import re
import time

from app.api_v1_2.domain.mobile_infos import Mobile
from app.api_v1_2.controller.core.adb import AndroidUtils


class Device(object):
    def __init__(self):
        self.android = AndroidUtils()
        self.minfo = Mobile()

    def get_devices(self):
        '''
        获取连接上电脑的手机设备，返回一个设备名的list
        '''
        sno_list = self.android.device_list()
        return sno_list

    def get_devices_as_dict(self):
        '''
        根据不同的需求，设计了返回dict和list格式的两个function。
        '''
        try:
            info = []
            lists = self.get_devices()
            if not lists or len(lists) <= 0:
                return None
            for sno in lists:
                info.append(self.get_info(sno))
            return {'data': info}
        except TypeError, e:
            return None

    def get_info(self, sno):
        '''
        通过adb命令来获取连接上电脑的设备的信息。
        '''
        self.minfo.sno = sno
        try:
            result = self.android.shell(sno, "cat /system/build.prop").stdout.readlines()
            for res in result:
                # 系统版本
                if re.search(r"ro\.build\.version\.release", res):
                    self.minfo.os_version = res.split('=')[-1].strip()
                # 手机型号
                elif re.search(r"ro\.product\.model",res) :
                    self.minfo.phone_model = res.split('=')[-1].strip()
                # 手机品牌
                elif re.search(r"ro\.product\.brand",res):
                    self.minfo.phone_brand = res.split('=')[-1].strip()
                if self.minfo.os_version is not None and self.minfo.phone_model is not None and self.minfo.phone_brand is not None:
                    break

            self.minfo.ip = self.android.device_wifi_ip(sno)
            self.minfo.image_resolution = self.android.device_distinguishability(sno)
            self.minfo.dpi = self.android.shell(sno, "getprop ro.sf.lcd_density").stdout.read()
            self.minfo.ram = str(self.android.device_ram(sno)) + 'GB'
            return self.minfo
        except Exception, e:
            return None





