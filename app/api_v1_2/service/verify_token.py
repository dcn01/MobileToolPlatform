#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: verify_token.py
@time: 2017/10/16 0:00
"""
from app.api_v1_2.initial import request
from app.api_v1_2.initial import Resource
from app.api_v1_2.initial import marshal_with
from app.api_v1_2.domain.marshals.user_marshal import resource_fields
from app.api_v1_2.utils.safety import SecurityVerification


class VerifyTokenService(Resource):

    def __init__(self):
        self.sv = SecurityVerification()

    @marshal_with(resource_fields)
    def get(self):
        token = request.args.get('token')
        ret = self.sv.verify_token(token)
        if ret:
            return ret
        else:
            return 'error'
