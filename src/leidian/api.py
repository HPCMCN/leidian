# -*- coding: utf-8 -*-
# author: HPCM
# time: 2023/5/29 11:41
# file: api.py
import os
import time

from . import logger
from .player import LDPlayer
from .executors import ADBExecutor, ConsoleExecutor


class LDApi(object):

    def __init__(self, path):
        self.console = ConsoleExecutor(os.path.join(path, "ldconsole.exe"))
        self.adb = ADBExecutor(os.path.join(path, "adb.exe"))
        self.adb.get_devices()

    def get_vms(self):
        """
        获取全部虚拟机
        :return:
        """
        return self.console.list()

    def start(self, name):
        """
        启动模拟器
        :param name: str, 模拟器名称
        :return: bool
        """
        while True:
            try:
                player = LDPlayer(self.adb, self)
                player.register(self.console.launch(name))
                break
            except IndexError:
                pass
            time.sleep(0.5)
        return player

    def reboot(self, name):
        """
        重启模拟器
        :param name: str, 模拟器名称
        :return:
        """
        return self.console.reboot(name)

    def shutdown(self, name=None):
        """
        关闭模拟器
        :param name: str, 模拟器名称
        :return:
        """
        return self.console.shutdown(name)

    def create(self, name):
        """
        创建模拟器
        :param name: str, 模拟器名称
        :return:
        """
        self.console.create(name)
        return self.get_player(name)

    def clone(self, src, dst):
        """
        克隆一个模拟器
        :param src: 被克隆的模拟器
        :param dst: 需要创建的新模拟器名字
        :return:
        """
        self.console.clone(src, dst)
        return self.get_player(dst)

    def destroy(self, name):
        """
        销毁模拟器
        :param name: str, 模拟器名称
        :return:
        """
        return self.console.destroy(name)

    def rename(self, src, dst):
        """
        重命名模拟器
        :param src: 原模拟器名字
        :param dst: 需要修改为的名字
        :return:
        """
        return self.console.rename(src, dst)

    def set_window(self, name, w, h, dpi, rotate=1, lockwindow=0):
        """
        修改模拟的尺寸信息
        :param name: str, 模拟器名称
        :param w: int, 高度
        :param h: int, 宽度
        :param dpi: str, dpi
        :param rotate: int, 是否自动旋转 1/0
        :param lockwindow: int, 锁定window大小
        :return:
        """
        return self.console.set_window(name, w, h, dpi, rotate, lockwindow)

    def set_cpu(self, name, count):
        """
        修改cpu相关信息
        :param name: str, 模拟器名字
        :param count: int, cpu核数, 1, 2, 3, 4...
        :return:
        """
        return self.console.set_cpu(name, count)

    def modify_memory(self, name, size):
        """
        修改内存大小
        :param name: str, 模拟器名字
        :param size: int, 内存大小设置, 256 | 512 | 768 | 1024 | 1536 | 2048 | 4096 | 8192
        :return:
        """
        return self.console.set_memory(name, size)

    def set_root(self, name, state):
        """
        修改root的状态
        :param name: str, 模拟器名字
        :param state: int, 0/关闭, 1/开启
        :return:
        """
        return self.console.set_root(name, state)

    def set_mac(self, name, mac):
        """
        修改mac地址
        :param name: str, 模拟器名字
        :param mac: str, mac地址
        :return:
        """
        return self.console.execute(name, mac)

    def set_factory(self, name, manufacturer, model, pnumber, imei, imsi, simserial, androidid):
        """
        修改其他信息
        :param name, str, 模拟器名字
        :param manufacturer: str, 制造商信息
        :param model: str, 型号信息
        :param pnumber: str, 电话号码
        :param imei: str, IMEI码
        :param imsi: str IMSI码
        :param simserial: str, 产品序列号
        :param androidid: str, 安卓id
        :return:
        """
        return self.console.set_factory(name, manufacturer, model, pnumber, imei, imsi, simserial, androidid)

    def get_player(self, name):
        return LDPlayer(self.adb, self).register(name)
