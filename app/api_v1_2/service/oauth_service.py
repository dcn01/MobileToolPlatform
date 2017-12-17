#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: oauth_service.py
@time: 2017/12/14 22:55
"""
from datetime import datetime, timedelta
from app.api_v1_2.initial import Resource
from app.api_v1_2.initial import request
from app.api_v1_2.initial import reqparse
from app.api_v1_2.initial import marshal_with
from app.api_v1_2.initial import make_response, redirect
from app.api_v1_2.utils.safety import SecurityVerification


sv = SecurityVerification()
redirect_uri = 'http://localhost:5000/client/passport'
users = {"jay": ["zhen"]}
client_id = 'zhen'
users[client_id] = []
auth_code = sv.auth_code
oauth_redirect_uri = []


class OAuthentication(Resource):

    def __init__(self):
        super(OAuthentication, self).__init__()

    def post(self):
        return self.get()

    def get(self):
        # 处理表单登陆，同时设置cookie
        if request.method == "POST" and request.form['user']:
            print "处理表单登陆，并设置cookie"
            u = request.form['user']
            p = request.form['pw']
            print u, p
            if users.get(u)[0] == p and oauth_redirect_uri:
                uri = oauth_redirect_uri[0] + "?code=%s" % sv.gen_auth_code(oauth_redirect_uri[0], u)
                expire_date = datetime.now() + timedelta(minutes=1)
                resp = make_response(redirect(uri))
                print type(resp)
                resp.set_cookie("login", "_".join([u, p]), expires=expire_date)
                return resp

        # 验证授权码，发放token
        if request.args.get('code'):
            print "验证授权码，发放token"
            auth_info = auth_code.get(int(request.args.get("code")))
            print auth_info
            print request.args.get("redirect_uri")
            if auth_info[0] == request.args.get("redirect_uri"):
                # 可以子授权码的auth_code主公存储用户名，编进token中
                return sv.get_token(dict(client_id=request.args.get("client_id"), user_id=auth_info[1]))

        # 如果登陆用户有cookie，直接验证成功，否则需要填写登陆表单
        if request.args.get("redirect_uri"):
            print "处理重定向"
            oauth_redirect_uri.append(request.args.get("redirect_uri"))
            print request.cookies
            if request.cookies.get("login"):
                u, p = request.cookies.get("login").split("_")
                if users.get(u)[0] == p:
                    uri = oauth_redirect_uri[0] + "?code=%s" % sv.gen_auth_code(oauth_redirect_uri[0], u)
                    return redirect(uri)
            return make_response('''
                    <form action=" " method="post">
                        <p><input type='text' name='user'>
                        <p><input type='text' name='pw'>
                        <p><input type='submit' value='login'>
                    </form>
                    ''')