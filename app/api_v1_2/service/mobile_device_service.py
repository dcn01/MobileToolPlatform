#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: mobile_device_service.py
@time: 2017/10/22 16:24
"""

from app.api_v1_2.controller.device_cursor import Device
from app.api_v1_2.domain.marshals.mobile import mobile_marshal
from app.api_v1_2.excepts.network import *
from app.api_v1_2.initial import Resource, reqparse, marshal


class MobileInfoService(Resource):
    """
    手机信息获取：
    """
    endpoint_str = 'mobileinfo'

    def __init__(self):
        # 使用reqparse对请求进行验证
        self.reqparse = reqparse.RequestParser()
        # self.reqparse.add_argument('title', type = str, localtion = 'json', require = True, help = 'no title in request body')
        super(MobileInfoService, self).__init__()

    # @marshal_with(mobile_info)
    def get(self):
        mobile = Device()
        info = mobile.get_devices_as_dict()
        if info is None or info == "":
             return (CustomFlaskErr(10003, "Currently no device is connected to the server.")).to_dict()
        return marshal(info, mobile_marshal)
