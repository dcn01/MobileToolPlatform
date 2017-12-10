#!/usr/bin/env python
# -*- coding=utf8 -*-

from app.api_v1_2.service.mobile_device_service import MobileInfoService
from app.api_v1_2.service.mobile_runtime_service import MobileCursorService
from initial import create_app
from app.api_v1_2.configs.urls import URL


app, api = create_app('testing')

api.add_resource(MobileInfoService, URL[MobileInfoService.endpoint_str], endpoint=MobileInfoService.endpoint_str,)
api.add_resource(MobileCursorService, URL[MobileCursorService.endpoint_str], endpoint=MobileCursorService.endpoint_str)
api.init_app(app)

if __name__ == '__main__':
    app.run(host='192.168.1.109', port=5006)

