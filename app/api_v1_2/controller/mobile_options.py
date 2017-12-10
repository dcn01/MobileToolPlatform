#!/usr/bin/env python
# -*- encoding: utf-8  -*-

""" 
@version: v1.0 
@author: jayzhen 
@license: Apache Licence  
@contact: jayzhen_testing@163.com 
@site: http://blog.csdn.net/u013948858 
@software: PyCharm 
@time: 2017/11/05 23:29
"""

from app.api_v1_2.controller.device_cursor import Device


class EventController(object):
    def __init__(self, ):
        self.dinfoObj = Device()
        self.deviceInfo = self.dinfoObj.get_devices_as_dict()
        self.t = None

    def do_install(self,sno):
        # 获取要安装apk的绝对路径
        # 2016.12.7 修复因图形中的数据排序与list中的数据排序的不同引起的数据获取错误
        index = self.guiobj.lc_apk_info.GetFirstSelected()
        filename = self.guiobj.lc_apk_info.GetItemText(index)
        # filename = self.apk_list[index]
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)

        # 获取被安装apk设备的sno号
        choiseitemid = self.guiobj.lc_device_info.GetFocusedItem()
        if choiseitemid == -1:
            return
        phonemodel = self.guiobj.lc_device_info.GetItem(choiseitemid, col=1).GetText()
        # 执行安装
        for sno in self.deviceInfo:
            if self.deviceInfo[sno]["phone_model"] == phonemodel:
                self.pctrObj.install_one_device(sno,filepath,apkPackageName)
                break
                # pctrObj.is_has_package(sno,apkPackageName)

    def do_install_more(self,sno):
        # 获取要安装apk的绝对路径
        index = self.guiobj.lc_apk_info.GetFirstSelected()
        filename = self.guiobj.lc_apk_info.GetItemText(index)
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)
        # 获取被安装apk设备的sno号
        first = self.guiobj.lc_device_info.GetFirstSelected()
        while first != -1:
            phonemodel = self.guiobj.lc_device_info.GetItem(first, col=1).GetText()
            # 执行安装
            for sno in self.deviceInfo:
                if self.deviceInfo[sno]["phone_model"] == phonemodel:
                    self.pctrObj.install_one_device(sno,filepath,apkPackageName)
                    self.pctrObj.is_has_package(sno,apkPackageName)
            first = self.lc_device_info.GetNextSelected(first)

    def do_install_all(self,sno):
        index = self.guiobj.lc_apk_info.GetFirstSelected()
        filename = self.guiobj.lc_apk_info.GetItemText(index)
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)
        self.pctrObj.install_all_devices(filepath, apkPackageName)

    def do_cover_install(self,sno):
        # 获取要安装apk的绝对路径
        index = self.guiobj.lc_apk_info.GetFirstSelected()
        filename = self.guiobj.lc_apk_info.GetItemText(index)
        filepath = self.apkObj.apk_abs_path(filename)
        apkPackageName = self.apkObj.get_apk_package_name(filepath)
        # 获取被安装apk设备的sno号
        choiseitemid = self.guiobj.lc_device_info.GetFocusedItem()
        if choiseitemid == -1:
            return
        phonemodel = self.guiobj.lc_device_info.GetItem(choiseitemid, col=1).GetText()
        # 执行安装
        for sno in self.deviceInfo:
            if self.deviceInfo[sno]["phone_model"] == phonemodel:
                self.pctrObj.cover_install(sno,filepath,apkPackageName)
                break
                #pctrObj.is_has_package(sno,apkPackageName)

    def do_clear_data(self, packagename):
        index = self.guiobj.lc_device_info.GetFirstSelected()
        if index == -1:
            return
        index = self.guiobj.lc_device_info.GetFirstSelected()
        phonemodel = self.guiobj.lc_device_info.GetItem(index, col=1).GetText()
        for sno in self.deviceInfo:
            if self.deviceInfo[sno]["phone_model"] == phonemodel:
                self.pctrObj.clear_app_data(sno, packagename)
                break

    def do_input_text(self,txt):
        choiseitemid = self.guiobj.lc_device_info.GetFocusedItem()
        if choiseitemid == -1:
            return
        phonemodel = self.guiobj.lc_device_info.GetItem(choiseitemid, col=1).GetText()
        # 弹出一个文本框提示输入信息
        # iptxt_obj = wx.TextEntryDialog(None,'in the "http://v.youku.com/" following',caption="Input to send messages to the phone",  style=wx.OK|wx.CANCEL|wx.CENTRE)
        flag = True
        for sno in self.deviceInfo:
            if self.deviceInfo[sno]["phone_model"] == phonemodel:
                self.dinfoObj.input_text(sno,txt)
                flag = False
        flag = False

    def do_reboot(self,sno):
        sno = self.get_device_items_choised_sno()
        if sno is None or sno == "":
            return
        self.dinfoObj.reboot_device(sno)

    def do_capture_window(self, sno):
        sno = self.get_device_items_choised_sno()
        if sno is None or sno == "":
            return
        self.dinfoObj.screencapture(sno)

    def get_app_crash_log(self,sno):
        sno = self.get_device_items_choised_sno()
        if sno is None or sno == "":
            return
        self.dinfoObj.get_crash_log(sno)

    def reset_service_port(self,sno):
        self.dinfoObj.win_serivce_port_restart()

    def do_screenrecord_sno(self,txt):
        sno = self.get_device_items_choised_sno()
        if sno is None or sno == "" :
            return
        self.thread_leader.run_thread("screenrecord", (sno, txt))

    def do_kill_process_sno(self, sno):
        sno = self.get_device_items_choised_sno()
        pkg = self.dinfoObj.current_package_name(sno)
        self.dinfoObj.do_kill_process(sno,pkg)

