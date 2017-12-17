#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: mobile.py
@time: 2017/10/22 16:34
"""

from datetime import datetime
from app.api_v1_2.initial import fields

lists = {
    "Key": fields.String(default=""),
    "Level": fields.String(default=""),
    "Memo": fields.String(default=""),
    "Title": fields.String(default="")
}

info = {
     'permissions': fields.List(fields.Nested(lists), attribute='app_permission', default=''),
     'package': fields.String(attribute='curt_pkg', default=''),
     'activity': fields.String(attribute='curt_act', default=''),
     'screenStatus': fields.String(attribute='screen_status', default=''),
     'wifiStatus': fields.String(attribute="wifi_status", default=''),
     'cpu': fields.String(attribute="curt_cpu", default=''),
     'mem': fields.String(attribute='curt_mem', default=''),
     'battery': fields.String(attribute='curt_battery', default=''),
    }


runtime_marshal = {
    'url': fields.Url('mobilecursor', absolute=True, scheme='http', ),
    'message': fields.String(default='mobile runtime infos'),
    # 'data': fields.List(fields.Nested(info), default=None),   # 上面需要对每个字段都进行校验
    'data': fields.Raw(default=None),  # 这个改动表示原数据中的data信息会原封不动的返回给请求者
    'date': fields.DateTime(default=str(datetime.now())),
    'status': fields.Boolean(default=True),
 }
