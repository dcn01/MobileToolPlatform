#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@time: 2017/10/22 22:39
"""
import copy
from app.api_v1_2.domain.app_infos import App
from app.api_v1_2.configs.status_enum import runtime_attribute
from app.api_v1_2.domain.runtime_infos import Runtime
from app.api_v1_2.excepts.custom_error import CustomFlaskErr


def obj_2_dict(obj):
    pr = {}
    for name in dir(obj):
        value = getattr(obj, name)
        if not name.startswith('__') and not callable(value):
            pr[name] = value
    return pr


def dict_2_obj(d):
    top = type('new', (object,), d)
    seqs = tuple, list, set, frozenset
    for i, j in d.items():
        if isinstance(j, dict):
            setattr(top, i, dict_2_obj(j))
        elif isinstance(j, seqs):
            setattr(top, i, type(j)(dict_2_obj(sj) if isinstance(sj, dict) else sj for sj in j))
        else:
            setattr(top, i, j)
    return top

'''
对于接口字段来说，如果接口中的字段是必传，那么使用fire方法合适，这样只要有空的字段就报错
如果接口字段不重要且可以为空，那么在为空或None的时候就不传，使用water方法
'''


def chk_attr_fire(obj):
    '''
    火比较暴力，有错就返回对应的错误
    :param obj:
    :return:
    '''
    objdict = obj_2_dict(obj)
    for i in objdict:
        if objdict[i] is None or objdict[i] == "":
            return runtime_attribute[i]
    return True


def chk_attr_water(obj):
    '''
    水比较柔和，有错误就打印，返回可用的数据
    :param obj:
    :return:
    '''
    objdict = obj_2_dict(obj)
    newdict = copy.deepcopy(objdict)
    for i in objdict:
        if objdict[i] is None or objdict[i] == "":
            # print runtime_attribute[i]
            newdict.pop(i)
    return newdict



# if __name__ == '__main__':
#     app = Runtime()
#     app.curt_act = '1'
#     app.screen_status = '2'
#     app.curt_pkg='3'
#     app.app_permission = '4'
#     app.curt_battery= '5'
#     app.curt_cpu = '6'
#     app.curt_mem = '7'
#     app.wifi_status = ''
#     err = chk_attr_fire(app)
#     print err
#     if err != True:
#         print CustomFlaskErr(err[0], err[1]).to_dict()
#
#     print chk_attr_water(app)