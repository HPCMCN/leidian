# -*- coding: utf-8 -*-
# author: HPCM
# time: 2023/5/29 11:41
# file: player.py
from .executors import ADBExecutor


class LDPlayer(object):

    def __init__(self, adb, control=None):
        self.adb = adb or ADBExecutor
        self.control = control
        self.device = None
        self.name = None

    def register(self, name):
        """
        连接指定模拟器
        :param name: str, 模拟器名字
        :return:
        """
        self.device = self.control.console.get_device(name)
        self.name = name
        self.connect(self.device)
        return self

    def connect(self, ip_or_dns):
        """
        连接adb服务
        :param ip_or_dns: str, IP端口组合, 或者dns
        :return:
        """
        return self.adb.connect(ip_or_dns)

    def disconnect(self, ip_or_dns):
        """
        断开adb服务
        :param ip_or_dns: str, IP端口组合, 或者dns
        :return:
        """
        return self.adb.disconnect(ip_or_dns)

    def app_list(self):
        """
        查看 APP 列表
        :return:
        """
        return self.adb.app_list(self.device)

    def app_detail(self, app):
        """
        查看app详细信息
        :param app:
        :return:
        """
        return self.adb.detail(self.device, app)

    def app_start(self, name):
        """
        启动某个app
        :param name:
        :return:
        """
        return self.adb.app_start(self.device, name)

    def screen(self, filename=None):
        """
        手机截屏
        :param filename: str, 需要保存的位置
        :return: stream or png file
        """
        return self.adb.screen(self.device, filename)

    def input(self, text):
        """
        向模拟器中输入字符
        :param text: str, 需要输入的内容
        :return:
        """
        return self.control.console.input(self.name, text)

    def click(self, x, y):
        """
        点击事件
        :param x: int
        :param y: int
        :return:
        """
        return self.adb.click(self.device, x, y)

    def swipe(self, sx, sy, ex, ey, microseconds):
        """
        滑动屏幕
        :param sx: int, 起始x
        :param sy: int, 起始y
        :param ex: int, 结束x
        :param ey: int, 结束y
        :param microseconds: int, 持续时长, 单位毫秒
        :return:
        """
        return self.adb.swipe(self.device, sx, sy, ex, ey, microseconds)

    def __str__(self):
        return f"<Player {self.name} --> {self.device}>"
