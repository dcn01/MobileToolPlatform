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
from app.api_v1_2.utils.apkFileUtil import ApkController


class ApkOptService(Resource):

    endpoint_str = "apkopt"

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.apkctl = ApkController()
        super(ApkOptService, self).__init__()

    def get(self):
        self.reqparse.add_argument('id', dest='id', type=str, location='args', required=True, help='the mobile serie number is requred')
        self.reqparse.add_argument('type', dest='type', type=str, location='args', required=True, help='the option type is required')
        args = self.reqparse.parse_args()
        if args["type"] == "list":
            file_list = self.apkctl.apk_list()
            fpath, fname, fmtime = self.apkctl.get_latest_apk(file_list)
            pkg_name = self.apkctl.get_apk_package_name(fpath)
            dicts = {}
            dicts['fname'] = fname
            dicts['fpath'] = fpath
            dicts['pkgname'] = pkg_name
            dicts['fmtime'] = fmtime

            return {"apkfilelist": file_list, "latestfile": dicts}