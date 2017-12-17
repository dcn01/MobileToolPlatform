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


class UnreadItem(fields.Raw):
    """
    继承fields.raw 自定义蒙版字段类型
    """
    def format(self, value):
        return "True" if value & 0x02 else "False"

# 会被蒙版过滤的部分
info = {
     'id': fields.String(attribute='sno', default=None),
     'brand': fields.String(attribute='phone_brand', default=None),
     'model': fields.String(attribute='phone_model', default=None),
     'version': fields.String(attribute='os_version', default=None),
     'ram': fields.String(default=None),
     'dpi': fields.String(default=None),
     'resolution': fields.String(attribute='image_resolution', default=None),
     'address': fields.String(attribute='ip', default=None),
    }


mobile_marshal = {
    'url': fields.Url('mobileinfo', absolute=True, scheme='http', ),
    'message': fields.String(default='mobile infos'),
    'data': fields.List(fields.Nested(info), default=None),
    'date': fields.DateTime(default=str(datetime.now())),
    'status': fields.Boolean(default=True),
 }
