# -*- coding: utf-8 -*-
from time import sleep
from app.api_v1_2.controller.core.adb import AndroidUtils
import threading
#!/usr/bin/env python
# -*- encoding: utf-8  -*-

""" 
@version: v1.0 
@author: jayzhen 
@license: Apache Licence  
@contact: jayzhen_testing@163.com 
@site: http://blog.csdn.net/u013948858 
@software: PyCharm 
@time: 2017/7/24 23:29 
"""

# TODO(jayzhen) 电量专项测试，需要造个小轮子

class BatteryTemperature(threading.Thread):
    """
    获取手机电池的温度
    """
    def __init__(self):
        super(BatteryTemperature, self).__init__()
        self.ls = []

    def run(self):
        while True:
            if utils.stop!=True:
                break
            sleep(1)
            y = []
            dictionaries = {}
            tm = utils.timestamp()
            result = utils.shell("dumpsys battery").stdout.readlines()
            for i in result[1:]:
                new = i.split(":")
                dictionaries[new[0].strip()] = new[1].strip()
            y.append(tm)
            y.append("".join(list(dictionaries["temperature"])[0:2])+"."+"".join(list(dictionaries["temperature"])[2:]))
            self.ls.append(y)

    def get_battery_temp(self):
        return self.ls


if __name__ == '__main__':
    t = BatteryTempData(3)
    t.start()
    t.join()
