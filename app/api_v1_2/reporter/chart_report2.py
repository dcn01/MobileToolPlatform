#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: chart_report2
@time: 2018/4/11  17:43
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
C:\Users\user\.spyder2\.temp.py
"""
"""
Show how to modify the coordinate formatter to report the image "z"
value of the nearest pixel given x and y
"""
# coding: utf-8

import time
import string
import os
import math
import pylab

import numpy as np
from numpy import genfromtxt
import matplotlib
import matplotlib as mpl
from matplotlib.colors import LogNorm
from matplotlib.mlab import bivariate_normal

import matplotlib.pyplot as plt
import matplotlib.cm as cm

import matplotlib.animation as animation

metric = genfromtxt('D:\export.csv', delimiter=',')

lines = len(metric)
# print len(metric)
# print len(metric[4])
# print metric[4]

rowdatas = metric[:, 0]
for index in range(len(metric[4]) - 1):
    a = metric[:, index + 1]
    rowdatas = np.row_stack((rowdatas, a))

# print len(rowdatas)
# print len(rowdatas[4])
# print rowdatas[4]
#

# plt.figure(figsize=(38,38), dpi=80)
# plt.plot(rowdatas[4] )
# plt.xlabel('time')
# plt.ylabel('value')
# plt.title("USBHID data analysis")
# plt.show()

linenum = 1
##如果是参数是list,则默认每次取list中的一个元素,即metric[0],metric[1],...
listdata = rowdatas.tolist()
print listdata[4]

# fig = plt.figure()
# window = fig.add_subplot(111)
# line, = window.plot(listdata[4] )

fig, ax = plt.subplots()
line, = ax.plot(listdata[4], lw=2)
ax.grid()

time_template = 'Data ROW = %d'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)


# ax = plt.axes(xlim=(0, 700), ylim=(0, 255))
# line, = ax.plot([], [], lw=2)

def update(data):
    global linenum
    line.set_ydata(data)
    #    print 'this is line: %d'%linenum
    time_text.set_text(time_template % (linenum))
    linenum = linenum + 1
    #    nextitem = input(u'输入任意字符继续: ')
    return line,


def init():
    #    ax.set_ylim(0, 1.1)
    #    ax.set_xlim(0, 10)
    #    line.set_data(xdata)
    plt.xlabel('time')
    plt.ylabel('Time')
    plt.title('USBHID Data analysis')
    return line,


ani = animation.FuncAnimation(fig, update, listdata, interval=1 * 1000, init_func=init, repeat=False)
plt.show()


