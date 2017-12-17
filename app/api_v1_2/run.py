#!/usr/bin/env python
# -*- coding=utf8 -*-

from app.api_v1_2.service.mobile_device_service import MobileInfoService
from app.api_v1_2.service.mobile_runtime_service import MobileCursorService
from app.api_v1_2.service.mobile_apk_service import ApkOptService
from initial import create_app, redirect, request
from app.api_v1_2.configs.urls import URL
from app.api_v1_2.service.oauth_service import OAuthentication
from app.api_v1_2.service.verify_token import VerifyTokenService
from app.api_v1_2.utils.safety import SecurityVerification


app, api = create_app('testing')
sv = SecurityVerification()

redirect_uri = 'http://localhost:5000/client/passport'
users = {"jay": ["zhen"]}
client_id = 'zhen'
users[client_id] = []
auth_code = sv.auth_code
oauth_redirect_uri = []


# 客户端
@app.route("/client/login", methods=["POST", "GET"])
def client_login():
    uri = 'http://localhost:5000/oauth?response_type=code&client_id=%s&redirect_uri=%s' % (client_id, redirect_uri)
    return redirect(uri)


@app.route("/client/passport", methods=["POST", "GET"])
def client_passport():
    code = request.args.get("code")
    uri = 'http://localhost:5000/oauth?grant_type=authoriztion_code&client_id=%s&redirect_uri=%s&code=%s' %(client_id, redirect_uri, code)
    return redirect(uri)

api.add_resource(MobileInfoService, URL[MobileInfoService.endpoint_str], endpoint=MobileInfoService.endpoint_str,)
api.add_resource(MobileCursorService, URL[MobileCursorService.endpoint_str], endpoint=MobileCursorService.endpoint_str)
api.add_resource(ApkOptService, URL[ApkOptService.endpoint_str], endpoint=ApkOptService.endpoint_str)
api.add_resource(VerifyTokenService, '/test2')
api.add_resource(OAuthentication, '/oauth')
api.init_app(app)

if __name__ == '__main__':
    app.run(port=5006)

