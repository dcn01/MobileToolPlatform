#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: mobile_apk_service
@time: 2017/12/13  19:27
"""
from app.api_v1_2.initial import Resource, marshal, reqparse, request


class ApkOptService(Resource):

    endpoint_str = "apkopt"

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(ApkOptService, self).__init__()

    def get(self):
        self.reqparse.add_argument('id', dest='id', type=str, location='args', required=True, help='the mobile serie number is requred')
        self.reqparse.add_argument('type', dest='type', type=str, location='args', required=True, help='the option type is required')
        args = self.reqparse.parse_args()
        if args["type"] == "runtime" and args["id"] is not None and args["id"] != "":


            return None