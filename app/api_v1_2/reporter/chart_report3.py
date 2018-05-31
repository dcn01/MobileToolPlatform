#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@version: v1.0
@author: jayzhen
@license: Apache Licence 
@email: jayzhen_testing@163.com
@software: PyCharm
@file: chart_report3
@time: 2018/4/11  17:45
"""

import numpy as np
import wx
from matplotlib.figure import Figure
import matplotlib.font_manager as font_manager
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from meminfo import dumpsys_meminfo

# wxWidgets object ID for the timer
TIMER_ID = wx.NewId()
# number of data points
POINTS = 100


class WinGui(wx.Frame):
    """Matplotlib wxFrame with animation effect"""

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="App Perforence Usage Monitor", size=(1000, 800))
        # Matplotlib Figure   分辨率
        self.fig = Figure((10, 8), 100)
        # bind the Figure to the backend specific canvas
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.fig)
        # add a subplot
        self.ax = self.fig.add_subplot(1, 1, 1)
        # limit the X and Y axes dimensions
        self.ax.set_ylim([100, 2000])
        self.ax.set_xlim([0, POINTS])

        self.ax.set_autoscale_on(False)
        self.ax.set_xticks([])
        # we want a tick every 10 point on Y (101 is to have 10
        self.ax.set_yticks(range(100, 2001, 100))
        # disable autoscale, since we don't want the Axes to ad
        # draw a grid (it will be only for Y)
        self.ax.grid(True)
        # generates first "empty" plots
        self.user = [None] * POINTS
        self.l_user, = self.ax.plot(range(POINTS), self.user, label='app memifo %', marker='o')

        # add the legend
        self.ax.legend(loc='upper center',
                       ncol=4,
                       prop=font_manager.FontProperties(size=15))
        # force a draw on the canvas()
        # trick to show the grid and the legend
        self.canvas.draw()
        # save the clean background - everything but the line
        # is drawn and saved in the pixel buffer background
        self.bg = self.canvas.copy_from_bbox(self.ax.bbox)
        # bind events coming from timer with id = TIMER_ID
        # to the onTimer callback function
        wx.EVT_TIMER(self, TIMER_ID, self.onTimer)

    def onTimer(self, evt):
        """callback function for timer events"""
        # restore the clean background, saved at the beginning
        self.canvas.restore_region(self.bg)
        # update the data: x轴的数据一直变化
        # temp = np.random.randint(70, 90)
        temp = dumpsys_meminfo(process='com.youdao.dict')
        print temp
        self.user = self.user[1:] + [temp]
        # update the plot
        self.l_user.set_ydata(self.user)
        # just draw the "animated" objects
        # It is used to efficiently update Axes data (axis ticks, labels, etc are not updated)
        self.ax.draw_artist(self.l_user)
        self.canvas.blit(self.ax.bbox)


if __name__ == '__main__':
    app = wx.App()  # 实例一个app应用
    frame = WinGui()    # 这个界面会在app应用上展示
    t = wx.Timer(frame, TIMER_ID)    # 定时器有更新的界面和id
    t.Start(500)
    frame.Show()
    app.MainLoop()