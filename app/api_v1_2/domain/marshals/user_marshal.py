#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: user_marshal.py
@time: 2017/10/15 23:56
"""
from app.api_v1_2.initial import fields
from datetime import datetime

# marshal 蒙版
resource_fields = {
    'client_id': fields.String(default=""),
    'expires': fields.Float(default=0.0),
    'salt': fields.Float(default=0.0),
    'user_id': fields.String(default=""),
    'date': fields.DateTime(default=str(datetime.now()))
}

