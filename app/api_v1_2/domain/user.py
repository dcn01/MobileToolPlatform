#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: user.py
@time: 2017/10/15 15:51
"""


class User(object):
    def __init__(self, client_id, expires, salt, user_id):
        self.client_id = client_id
        self.expires = expires
        self.salt = salt
        self.user_id = user_id
