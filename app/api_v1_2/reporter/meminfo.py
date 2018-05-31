#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import subprocess
import sys
import re


class MemInfo:
    patternProcess = re.compile(r'\*\* MEMINFO in pid (\d+) \[(\S+)] \*\*')
    patternTotalPSS = re.compile(r'\s+TOTAL\s+(\d+)')  # 可能新的os系统没有`:`

    pid = 0
    processName = ''
    datetime = ''
    totalPSS = 0

    def __init__(self, dump):
        self.dump = dump
        self._parse()

    def _parse(self):
        match = self.patternProcess.search(self.dump)
        if match:
            self.pid = match.group(1)
            self.processName = match.group(2)
        match = self.patternTotalPSS.search(self.dump)
        if match:
            self.totalPSS = match.group(1)


def dumpsys_meminfo(process):
    """
    获取运行时占用的内存：
    :param process: pid 或 packageName
    :return: 标准输出的数据给对象解析，并返回对象实例
    """
    proc = subprocess.Popen(args='adb shell dumpsys meminfo "' + process + '"', stdout=subprocess.PIPE, stderr=sys.stderr, shell=True)
    out = proc.communicate()[0]
    mem_info = MemInfo(dump=out.decode(encoding='windows-1252'))
    if mem_info.dump == '':
        return 0
    elif mem_info.dump.startswith('No process found for:'):
        return 0
    # 返回的数据一定要是int或float类型的，不然matplotlib在update的时候会报错
    print mem_info.totalPSS
    return int(mem_info.totalPSS) / 1024

