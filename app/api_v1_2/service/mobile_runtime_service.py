#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: mobile_runtime_service.py
@time: 2017/11/5 23:32
"""

from app.api_v1_2.controller.device_cursor import Device
from app.api_v1_2.controller.runtime_cursor import AppRuntime
from app.api_v1_2.domain.marshals.runtime import runtime_marshal
from app.api_v1_2.excepts.custom_error import CustomFlaskErr
from app.api_v1_2.initial import Resource, reqparse, marshal
from app.api_v1_2.utils.obj2dict import chk_attr_water, chk_attr_fire


class MobileCursorService(Resource):

    endpoint_str = 'mobilecursor'

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.device = Device()
        super(MobileCursorService, self).__init__()

    def get(self):
        """
        20171106 实现从get请求的url ？后获取参数并把解析处理返回数据
        20171121 将数据获取抽离出去
        """
        app = AppRuntime()
        # http://192.168.1.107:15004/api/v1.2/mobile/cursor?id=90d1894b7d62&type=pkg
        self.reqparse.add_argument('id', dest='id', type=str, location='args', required=True, help='The id is null')
        self.reqparse.add_argument('type', dest='type', type=str, location='args', required=True, help='The type is null')
        args = self.reqparse.parse_args()

        if args["type"] == "runtime" and args["id"] is not None and args["id"] != "":
            res = app.get_infos(args["id"])
            if res is None:
                return CustomFlaskErr(10008, "Check if your device is connected properly").to_dict()
            data = chk_attr_water(res)
            # if data != True:
            #     return CustomFlaskErr(data[0], data[1]).to_dict()
            return marshal({"data": data}, runtime_marshal)

        return {'message': 'check you get method param'}

