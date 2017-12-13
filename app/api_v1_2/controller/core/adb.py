#!/usr/bin/env python
# -*- encoding: utf-8  -*-

""" 
@version: v1.0 
@author: jayzhen 
@license: Apache Licence  
@contact: jayzhen_testing@163.com 
@site: http://blog.csdn.net/u013948858 
@software: PyCharm 
@time: 2017/7/27 23:29
update 2017/11/21
"""
from __future__ import division
import _winreg
import json
import os
import platform
import re
import string
import subprocess
import sys
import time

import exception
from app.api_v1_2.utils.func_deprecated import deprecated
from app.api_v1_2.utils.filePathUtil import FilePathGetter
from permission import android_permissions

reload(sys)
sys.setdefaultencoding('utf8')


class AndroidUtils(object):
    def __init__(self):
        self.system = None
        self.find_type = None
        self.command = "adb"
        self.fp = FilePathGetter()

    def get_win_destop_path(self):
        try:
            # 通过python内置_winreg方法进行注册表的访问，从而获取桌面路径
            key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
            p = _winreg.QueryValueEx(key, "Desktop")[0]

            if p is None or p == "":
                usr = os.path.expanduser('~')
                plat = platform.system()
                desktop = ''
                if plat == 'Windows':
                    desktop = r'\Desktop'
                return usr + desktop
            return p
        except Exception, e:
            print e

    def judgment_system_type(self):
        # 判断系统类型，windows使用findstr，linux使用grep
        self.system = platform.system()
        if self.system is "Windows":
            self.find_type = "findstr"
        else:
            self.find_type = "grep"

    def judgment_sys_env_var(self):
        self.judgment_system_type()
        # 判断是否设置环境变量ANDROID_HOME
        if "ANDROID_HOME" in os.environ:
            if self.system == "Windows":
                self.command = "adb"   # os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb.exe")
            else:
                self.command = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", "adb")
        else:
            raise EnvironmentError(
                "Adb not found in $ANDROID_HOME path: %s." %os.environ["ANDROID_HOME"])

    # adb命令
    def adb(self, serialno_num, args):
        cmd = "%s -s %s %s" % (self.command, serialno_num, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # adb shell命令
    def shell(self, serialno_num, args):
        cmd = "%s -s %s shell %s" % (self.command, serialno_num, str(args))
        return subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def app_pid(self, sno, pkg_name):
        '''
        获取对应包名的pid
        :param sno:
        :param pkg_name:
        :return:
        '''
        self.judgment_system_type()
        if self.system is "Windows":
            strs = self.shell(sno, "ps | findstr %s$" % pkg_name).stdout.read()
        else:
            strs = self.shell(sno, "ps | grep -w %s" % pkg_name).stdout.read()
        if strs == '':
            return "the process doesn't exist."
        pattern = re.compile(r"\d+")
        result = strs.split(" ")
        result.remove(result[0])
        return pattern.findall(" ".join(result))[0]

    def app_uid(self, sno, pkg):
        """
        获取某一个应用的uid
        """
        # (jayzhen) 记得加一个多设备的兼容和异常 已完成  20170728
        pid = self.app_pid(sno, pkg)
        print pid
        res = self.shell(sno, "cat /proc/%s/status | findstr Uid" % pid).stdout.readline()
        return res.split("\t")[2]

    def app_cpu(self, sno, pkg):
        '''获取APP的CPU使用率'''
        cpu = "dumpsys cpuinfo|grep " + pkg + "|gawk '{print $1,$3,$6}'|sed 's/%//g'"
        return cpu

    def app_mem(self, sno, pkg):
        mem = "dumpsys meminfo " + pkg + "|gawk '/MEMINFO/,/App Summary/'|grep TOTAL|gawk '{print $2,$3,$4,$5,$6,$7,$8}'"
        return mem

    def app_gfx(self, sno, pgk):
        '''获取APP的GFX数据'''
        gfx = "dumpsys gfxinfo " + self.focused_package_and_activity(sno) + "|gawk '/Execute/,/Stats/'|gawk NF'{print $1,$2,$3,$4}'|grep -v '^Draw'|grep -v '^Stats'|sed '$d'"
        return gfx

    def app_net(self, sno, pkg):
        '''获取APP的流量'''
        net = "cat /proc/net/xt_qtaguid/stats|grep " + self.app_uid() + "|gawk '{rx_bytes+=$6}{tx_bytes+=$8}END{print rx_bytes,tx_bytes}'"
        return net

    def app_bat(self, sno, pkg):
        '''获取APP的电量'''
        bat = "dumpsys batterystats|grep " + pkg
        return bat

    def app_fps(self, sno, pkg):
        '''获取APP的FPS'''
        fps = "service call SurfaceFlinger 1013"
        return fps

    def app_permission_list(self, sno, package_name):
        '''
        2017.01.13 @pm # 获取设备上当前应用的权限列表
                   # Windows下会将结果写入permission.txt文件中，其他系统打印在控制台
        :param sno:
        :param package_name:
        :return:
        '''
        if sno or package_name is None:
            return None
        if sno or package_name == "":
            return None
        permission_list = []
        result_list = self.shell(sno, "dumpsys package %s | findstr android.permission" % package_name).stdout.readlines()
        for permission in result_list:
            permission_list.append(permission.strip())
        permission_json_file = file(self.fp.get_all_permission_file_path())
        file_content = json.load(permission_json_file)["PermissList"]
        name = "_".join(package_name.split("."))
        res_path = self.fp.get_app_performance_result_path("%s_permission.txt" % name)
        f = open(res_path, "w")
        f.write("package: %s\n\n" % package_name)
        for permission in permission_list:
            for permission_dict in file_content:
                if permission == permission_dict["Key"]:
                    f.write(permission_dict["Key"] + ":\n  " + permission_dict["Memo"] + "\n")
        f.close()

    def app_permission_dict(self, sno, package_name):
        """
        20171108 数据还有缺失需要补充源文件中的权限内容，提供给接口使用
        """
        if sno is None or sno == "":
            return None
        if package_name is None or package_name == "":
            return None
        app_permis = []
        result_list = self.shell(sno, " dumpsys package %s | findstr android.permission" % package_name).stdout.readlines()
        for permission in result_list:
            app_permis.append(permission.strip())
        perms_d = []
        for ap in app_permis:
            for dp in android_permissions:
                if ap == dp["Key"]:
                    perms_d.append(dp)
        if perms_d is not None and len(perms_d) > 0:
            return perms_d
        return None

    def device_state(self, sno):
        '''
        获取设备状态
        :param sno:
        :return: offline | bootloader | device
        '''
        return self.adb(sno, "get-state").stdout.read().strip()

    def device_list(self):
        devices = []
        result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
        # 将readlines结果反向排序
        result.reverse()
        for line in result[1:]:
            if "attached" not in line.strip() and "device" in line.strip():
                devices.append(line.split()[0])

        return devices

    def device_crash_log(self, sno):
        # 获取app发生crash的时间列表
        time_list = []
        result_list = self.shell(sno,"dumpsys dropbox | findstr data_app_crash").stdout.readlines()
        for time in result_list:
            temp_list = time.split(" ")
            temp_time= []
            temp_time.append(temp_list[0])
            temp_time.append(temp_list[1])
            time_list.append(" ".join(temp_time))

        if time_list is None or len(time_list) <=0:
            return None
        log_file = self.fp.get_exception_logs_file_path("Exception_log_%s.txt" %self.timestamp())
        f = open(log_file, "wb")
        for time in time_list:
            cash_log = self.shell(sno,"dumpsys dropbox --print %s" %time).stdout.read()
            f.write(cash_log)
        f.close()

    def device_wifi_ip(self, sno):
        """
        20170512 jayzhen 因为有些手机在getprop中无法获取到ip，那么就使用ifconfig命令，这种情况出现在Android6.0系统以上
        :param sno: 手机的唯一id
        :return: 手机的wifi下的网络ip
        """
        ip = self.shell(sno, "getprop dhcp.wlan0.ipaddress").stdout.read()
        if len(ip) < 5:
            res = self.shell(sno, "ifconfig wlan0").stdout.readlines()
            ip = (res[1].strip().split(" ")[1]).split(":")[1]
        return ip.strip()

    def device_distinguishability(self, sno):
        """
        20170512 jayzhen 调整获取分辨率的方式
        :param sno:
        :return: image_resolution
        """
        res_4_2 = self.shell(sno, "dumpsys window").stdout.read()
        r_4_2 = "init=(\d*x\d*)"
        reg_4_2 = re.compile(r_4_2)
        image_list_4_2 = re.findall(reg_4_2, res_4_2)
        if len(image_list_4_2) > 0:
            image_resolution = image_list_4_2[0]
        else:
            res_4_4 = self.shell(sno, "wm size").stdout.read()
            r_4_4 = "Physical size: (\d*x\d*)"
            reg_4_4 = re.compile(r_4_4)
            image_list_4_4 = re.findall(reg_4_4, res_4_4)
            image_resolution = image_list_4_4[0]
            if len(image_list_4_4) < 0:
                image_resolution = "NULL"
        return image_resolution

    def device_cpu_model(self, sno):
        '''
        cpu型号
        '''
        return self.shell(sno, "cat /proc/cpuinfo|findstr Hardware").stdout.readline().strip().split(":")[1]

    def device_display_rate(self, sno):
        """
        与方法device_distinguishability相似，只是执行的命令不同
        :param sno:
        :return:
        """
        result = self.shell(sno, "dumpsys display | findstr DisplayDeviceInfo").stdout.readline().split(",")[1].strip()
        return result

    def device_brand(self, sno):
        '''
        获取手机的厂商名
        :param sno:
        :return:
        '''
        return self.shell(sno, "cat /system/build.prop | findstr ro.product.brand").stdout.readline().split("=")[1]

    def device_system_version(self, sno):
        '''
        获取当前手机的系统版本，如：6.0.1
        :param sno:
        :return:
        '''
        return self.shell(sno, "cat /system/build.prop | findstr ro.build.version.release").stdout.readline().split("=")[1]

    def device_sdk_version(self,sno):
        '''
        获取手机使用的sdk版本，如：22
        :param sno:
        :return:
        '''
        return self.shell(sno, "cat /system/build.prop | findstr ro.build.version.sdk").stdout.readline().split("=")[1]

    def device_cpu_max_frequency(self, sno):
        '''
        获取设备CPU最大频率
        :param sno:
        :return:
        '''
        max_frequency = self.shell(sno,"su -c 'cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq'").stdout.readline().strip()
        if "not found" in max_frequency:
            max_frequency = "Permission denied"
            return max_frequency
        else:
            return "{val}MHz".format(val=int(max_frequency) / 1000)

    def device_cpu_min_frequency(self, sno):
        '''
        获取设备CPU最小频率
        :param sno:
        :return:
        '''
        min_frequency = self.shell(sno, "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_min_freq").stdout.readline().strip()
        return "{val}MHz".format(val=int(min_frequency) / 1000)

    def device_ram(self, sno):
        """
        20170512 jayzhen 将获取手机运行内存的方式从device_info中隔离出来：使用四舍五入的方式，算的手机的运行内存：int(round(x))或int(2*x)/2+int(2*x)%2
        :param sno:
        :return:
        """
        try:
            proc_meninfo = self.shell(sno, 'cat /proc/meminfo |findstr MemTotal').stdout.readline()
            mem_size = int(proc_meninfo.split(" ")[-2])
            ram = int(round(mem_size / (1024 * 1024)))
            """
            ram = (int(proc_meninfo.split(" ")[-2])//1000000)
            if int(proc_meninfo.split(" ")[-2]) % 1000000 >= 500000:
                ram += 1
            """
            return ram
        except IndexError, e:
            ram = "X"
            return ram

    def kill_app_pid(self, sno, pid):
        '''
        杀掉对应包名的进程；另一个方式使用adb shell am force-stop pkg_name
        :param sno:
        :param pid:
        :return:
        '''
        result = self.shell(sno, "kill -9 %s" % str(pid)).stdout.read().split(": ")[-1]
        if result != "":
            raise exception.SriptException("Operation not permitted or No such process")

    def focused_package_and_activity(self, sno):
        '''
        获取设备上当前应用的包名与activity
        :param sno:
        :return:
        '''
        try:
            return self.shell(sno, "dumpsys activity | findstr mFocusedActivity").stdout.read().split()[-2]
        except IndexError, e:
            print 'get focuse package happend error : {}'.format(str(e))
    def current_package_name(self, sno):
        '''
        获取当前应用的包名
        :param sno:
        :return:
        '''
        return self.focused_package_and_activity(sno).split("/")[0]

    def current_activity(self, sno):
        '''
        获取当前设备的activity
        :param sno:
        :return:
        '''
        return self.focused_package_and_activity(sno).split("/")[-1]

    def current_running_activity(self, sno):
        '''
        2017.11.17 获取当前所有运行的活动（运行的app）
        '''
        log = self.shell(sno,"dumpsys activity activities").stdout.read()
        returnString = []
        startIndex = 0
        tempString = log.split('\n')
        for line in tempString:
            line = line.strip()
            if line:
                returnString.append(line)
        # 使用了枚举方式
        for index, line in enumerate(returnString):
            if "Running activities" in line:
                startIndex = index
                break
        returnList = returnString[startIndex:startIndex+3]
        return returnList[-1]

    def screen_record(self, sno, times, path):
        """
        2017.01.12 @pm 添加系统在4.4.x(sdk>19)以上手机可以进行截取屏幕视频动画的功能
                   @func 判断系统->执行任务->获取结果
        2017.07.13 @pm 修改导出文件的位置
        """
        PATH = lambda p: os.path.abspath(p)
        sdk = string.atoi(self.shell(sno, "getprop ro.build.version.sdk").stdout.read())
        try:
            times = string.atoi(times)
        except ValueError, e:
            times = int(20)
        if sdk >= 19:
                self.shell(sno, "screenrecord --time-limit %d /data/local/tmp/screenrecord.mp4"%times).wait()
                time.sleep(1.5)
                path = PATH(path)
                if not os.path.isdir(path):
                    os.makedirs(path)
                self.adb(sno, "pull /data/local/tmp/screenrecord.mp4 %s" % PATH("%s/%s.mp4" % (path, self.timestamp()))).wait()
                self.shell(sno, "rm /data/local/tmp/screenrecord.mp4")
        else:
            sys.exit(0)

    def screen_capture(self, sno):
        desktop_path = self.get_win_destop_path()
        self.shell(sno, "rm /sdcard/screenshot.png").wait()
        self.shell(sno, "/system/bin/screencap -p /sdcard/screenshot.png").wait()
        c_time = time.strftime("%Y_%m_%d_%H-%M-%S")
        file_path = os.path.join(desktop_path, '%s.png"'%c_time)
        self.adb(sno, 'pull /sdcard/screenshot.png %s' % file_path).wait()

    def kill_app_package(self, sno, specified_package):
        """
        2017.01.13 @pm 杀死进程同在设置中强制关闭一个程序
                   @func get到sno和package，进行命令执行
        """
        self.shell(sno, "am force-stop %s" % specified_package)

    def is_installed_package(self, sno, package_name):
        # (20170721jayzhen) 添加对app的检查，是否安装
        had_package = self.shell(sno, 'pm list packages | findstr "%s"' % package_name).stdout.read()
        if re.search(package_name, had_package):
            return True
        else:
            return False

    def is_running_package(self, sno, package_name):
        """
            20170703 jayzhen 查看指定的应用是否在运行
        """
        had_package = self.shell(sno, 'ps |findstr "%s"' % package_name).stdout.read()
        if re.findall(package_name, had_package):
            return True
        else:
            return False

    @deprecated
    def is_screen_locked_2(self, sno):
        """
        查看当前手机屏幕是什么状态：锁屏（0，1） * 亮黑（0，1）
        三种情况需要考虑
        2：黑屏上锁、0：亮屏解锁、1：亮屏上锁
        四种情况去考虑就是有无锁、是否亮屏，我觉得还是按其中来吧
        10:锁黑、11：锁亮、01：开亮、00：开黑
        adb shell dumpsys window policy | grep isStatusBarKeyguard 确认是否有锁
        adb shell dumpsys window policy | grep ScreenOn 是否亮屏
        """

        locked = self.shell(sno, "dumpsys window policy | grep isStatusBarKeyguard").stdout.readlines()
        bright = self.shell(sno, "dumpsys window policy | grep ScreenOn").stdout.readlines()
        locked_status = re.search(r"isStatusBarKeyguard=(\w+)", locked[0]).group(1).strip()
        bright_status = re.search(r"mScreenOnFully=(\w+)", bright[0]).group(1).strip()
        print locked_status, bright_status
        if locked_status == 'true' and bright_status == 'true':
            return "11"
        elif locked_status == 'true' and bright_status == 'false':
            return "10"
        elif locked_status == 'false' and bright_status == 'false':
            return "00"
        elif locked_status == 'false' and bright_status == 'true':
            return "01"

    def is_screen_locked(self, sno):
        window_policy = self.shell(sno, "dumpsys window policy").stdout.read()
        locked_status = re.findall(r"isStatusBarKeyguard=(\w+)", window_policy)[0]
        bright_status = re.findall(r"mScreenOnFully=(\w+)", window_policy)[0]

        if locked_status == 'true' and bright_status == 'true':
            return "11"
        elif locked_status == 'true' and bright_status == 'false':
            return "10"
        elif locked_status == 'false' and bright_status == 'false':
            return "00"
        elif locked_status == 'false' and bright_status == 'true':
            return "01"

    def input_text(self, sno, text):
        text_list = list(text)
        specific_symbol = set('&', '@', '#', '$', '^', '*')
        for i in range(len(text_list)):
            if text_list[i] in specific_symbol:
                if i-1 < 0:
                    text_list.append(text_list[i])
                    text_list[0] = "\\"
                else:
                    text_list[i-1] = text_list[i-1] + "\\"
        seed = ''.join(text_list)
        self.shell(sno, 'input text "%s"' % seed)

    def reboot_device(self, sno):
        self.adb(sno, "reboot")

    def disconnect_wifi(self, sno):
        """
            20170521 jayzhen 实现断网
            """
        self.shell(sno, "svc wifi disable")

    def connect_wifi(self, sno):
        self.shell(sno, "svc wifi enable")

    def timestamp(self):
        '''时间戳'''
        return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))

    def restart_5037(self):
        pid1 = os.popen("netstat -ano | findstr 5037 | findstr  LISTENING").read()
        if pid1 is not None:
            pid = pid1.split()[-1]
        # 下面的命令执行结果，可能因电脑而异，若获取adb.exe时出错，可自行调试！
        # E:\>tasklist /FI "PID eq 10200"
        # Image Name                     PID Session Name        Session#    Mem Usage
        # ========================= ======== ================ =========== ============
        # adb.exe                      10200 Console                    1      6,152 K
            process_name = os.popen('tasklist /FI "PID eq %s"' % pid).read().split()[-6]
            process_path = os.popen('wmic process where name="%s" get executablepath' %process_name).read().split("\r\n")[1]
        # #分割路径，得到进程所在文件夹名
        # name_list = process_path.split("\\")
        # del name_list[-1]
        # directory = "\\".join(name_list)
        # #打开进程所在文件夹
        # os.system("explorer.exe %s" %directory)
        # 杀死该进程
            os.system("taskkill /F /PID %s" % pid)
            os.system("adb start-server")
