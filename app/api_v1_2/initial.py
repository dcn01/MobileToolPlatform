#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: initial.py
@time: 2017/11/4 23:09
"""

from flask import Flask
from flask import make_response
from flask import jsonify
from flask import abort
from flask import redirect
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_restful import Api
from flask_restful import Resource
from flask_restful import marshal_with
from flask_restful import marshal
from flask_restful import reqparse
from flask_restful import request
from flask_restful import fields
from flask_sqlalchemy import SQLAlchemy
from app.api_v1_1.configs.factory_config import config

# 初始化Flask服务,和restful api

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
api = Api()
# 工厂函数实例app对象


def create_app(config_name):
    app = Flask(__name__)
    # app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from app.api_v1_2.excepts.network import network_errors
    app.register_blueprint(network_errors)

    # 附加路由和自定义的错误页面
    return app, api
