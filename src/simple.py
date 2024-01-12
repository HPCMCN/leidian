# -*- coding: utf-8 -*-
# author: HPCM
# time: 2024/1/12 15:43
# file: simple.py
from src.leidian.api import LDApi


# 启动模拟器
ld = LDApi(r"C:\Applications\leidian\LDPlayer9")
# player = ld.start("雷电模拟器")
player = ld.get_player("雷电模拟器")
print(player)

# 获取屏幕图片
# filename = player.screen("screen.png")
# image_object = player.screen()

# 获取应用列表
print(player.app_list())

# 点击屏幕
player.click()

# 滑动屏幕
player.swipe()