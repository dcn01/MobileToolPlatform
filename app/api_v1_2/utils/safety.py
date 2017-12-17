#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: safety.py
@time: 2017/10/15 23:45
"""
import base64
import random
import json
import time
import hmac


class SecurityVerification(object):

    def __init__(self):
        self.auth_code = {}
        self.TIMEOUT = 3600 * 2

    # 新版的token生成器
    def get_token(self, data):
        data = data.copy()
        if "salt" not in data:
            data["salt"] = unicode(str(random.random()).decode("ascii"))
        if "expires" not in data:
            data["expires"] = time.time() + self.TIMEOUT

        payload = json.dumps(data).encode("utf8")
        # 生成签名
        sig = self._get_signature(payload)
        return self.encode_token_bytes(payload + sig)

    # 授权码生成器
    def gen_auth_code(self, uri, user_id):
        code = random.randint(0, 10000)
        self.auth_code[code] = [uri, user_id]
        return code

    # 新版本的token验证
    def verify_token(self, token):
        decoded_token = self.decode_token_bytes(str(token))
        payload = decoded_token[:-16]
        sig = decoded_token[-16:]
        # 生成签名
        expected_sig = self._get_signature(payload)
        if sig != expected_sig:
            return {}
        data = json.loads(payload.decode("utf8"))
        if data.get('expires') >= time.time():
            return data
        return 0

    # 使用hmac为消息生成签名
    def _get_signature(self, value):
        return hmac.new("secret123456", value).digest()

    # 下面两个函数将base64编码和解码进行单独封装
    def encode_token_bytes(self, data):
        return base64.urlsafe_b64encode(data)

    def decode_token_bytes(self, data):
        return base64.urlsafe_b64decode(data)