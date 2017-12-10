#!/usr/bin/env python
# -*- coding=utf8 -*-

from flask import make_response, jsonify
from custom_error import CustomFlaskErr
from flask import Blueprint
network_errors = Blueprint('network_errors', __name__)

@network_errors.app_errorhandler(404)
def not_found(error):
    # return make_response('''<br/><br/><h1>NOT FOUND</h1>'''), 404
    return jsonify({"msg": '抱歉，你访问的接口不存在', "code": "404"}), 404

@network_errors.app_errorhandler(500)
def internal_error(error):
    # return make_response('''<br/><br/><h1>INTERNAL SERVER ERROR </h1>'''), 500
    return jsonify({"msg":'抱歉，服务器处理异常',"code":"500"}),500


@network_errors.app_errorhandler(CustomFlaskErr)
def custom_error(error):
    # response 的 json 内容为自定义错误代码和错误信息
    response = jsonify(error.to_dict())
    print error.to_dict()
    # response 返回 error 发生时定义的标准错误代码
    response.status_code = error.status_code
    return response

@network_errors.route("/net/status")
def custom():
    return make_response('''<br/><br/><h1>INTERNAL SERVER ERROR: testing </h1>''')

@network_errors.route('/')
def hello_world():
    return '''<br/><br/><h1 style="text-align:center">&nbsp;&nbsp;&nbsp;flask service is running . . .</h1>'''