# -*- coding: utf-8 -*-
# author: HPCM
# time: 2023/5/29 11:42
# file: executors.py
import os
import subprocess


class BaseExecutor(object):

    def __init__(self, executor_path=None):
        self.executor_path = executor_path

    @staticmethod
    def _shell_execute(cmd):
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        result = process.stdout.read()
        process.terminate()
        return result

    def execute(self, cmd, envs=None):
        raise NotImplementedError


class ADBExecutor(BaseExecutor):

    def execute(self, cmd, envs=None, stream=False):
        cmd = self.executor_path + " " + cmd
        print(f"adb: {cmd}")
        if envs:
            os.environ.update(envs)
        result = self._shell_execute(cmd)
        if not stream:
            result = result.decode()
        return result

    def get_devices(self):
        cmd = "devices"
        return [x.split() for x in self.execute(cmd).strip().split("\n") if "List of" not in x]

    def connect(self, ip_or_dns):
        cmd = f"connect {ip_or_dns}"
        return self.execute(cmd)

    def disconnect(self, ip_or_dns):
        cmd = f"disconnect {ip_or_dns}"
        return self.execute(cmd)

    def version(self):
        """
        查看adb版本信息
        :return:
        """
        cmd = "version"
        return self.execute(cmd)

    def app_list(self, device):
        """
        查看app列表
        :param device: 需要连接的设备
        :return:
        """
        cmd = f"shell pm list packages"
        return [x.strip() for x in self.execute(cmd, envs={"ANDROID_SERIAL": device}).strip().split("\n") if x]

    def app_detail(self, device, app):
        cmd = f"shell dumpsys package {app}"
        return self.execute(cmd, envs={"ANDROID_SERIAL": device})

    def app_start(self, device, app):
        cmd = f"shell am start {app}"
        return self.execute(cmd, envs={"ANDROID_SERIAL": device})

    def pull(self, device, src, dst):
        cmd = f"pull {src} {dst}"
        return self.execute(cmd, envs={"ANDROID_SERIAL": device})

    def screen(self, device, filename=None):
        cmd = f"shell screencap -p"
        res = self.execute(cmd, envs={"ANDROID_SERIAL": device}, stream=True)
        content = res.replace(b"\r\n", b"\n").replace(b"\r\r\n", b"\n")
        if filename:
            with open(filename, "wb+") as fp:
                fp.write(content)
            return os.path.abspath(filename)
        return content

    def click(self, device, x, y):
        cmd = f"shell input tap {x} {y}"
        return self.execute(cmd, envs={"ANDROID_SERIAL": device})

    def swipe(self, device, sx, sy, ex, ey, microseconds):
        cmd = f"shell input swipe {sx} {sy} {ex} {ey} {microseconds}"
        return self.execute(cmd, envs={"ANDROID_SERIAL": device})


class ConsoleExecutor(BaseExecutor):

    def execute(self, cmd, envs=None):
        cmd = self.executor_path + " " + cmd
        print(f"console: {cmd}")
        if envs:
            os.environ.update(envs)
        result = self._shell_execute(cmd)
        return result.decode("gbk")

    def list(self):
        cmd = "list2"
        data = []
        for x in self.execute(cmd).strip().split():
            if x.startswith("99999"):
                continue
            ld = x.strip().split(",")
            data.append({
                "index": ld[0],
                "name": ld[1],
                "top_fp": ld[2],
                "bind_fp": ld[3],
                "is_android": ld[4],
                "pid": ld[5],
                "box": ld[6],
                "resolution": f"{ld[7]}x{ld[8]}",
                "dpi": ld[9],
                "is_running": int(ld[5]) > 0
            })
        return data

    def launch(self, name):
        cmd = f"launch --name {name}"
        status = self.execute(cmd) == ""
        if not status:
            raise EnvironmentError("启动失败!")
        return name

    def shutdown(self, name=None):
        if name is None:
            cmd = "quitall"
        else:
            cmd = f"quit --name {name}"
        self.execute(cmd)

    def reboot(self, name):
        cmd = f"reboot --name {name}"
        return self.execute(cmd)

    def create(self, name):
        cmd = f"add --name {name}"
        return self.execute(cmd)

    def clone(self, src, dst):
        cmd = f"copy --name {dst} --from {src}"
        return self.execute(cmd)

    def destroy(self, name):
        cmd = f"remove --name {name}"
        return self.execute(cmd)

    def rename(self, src, dst):
        cmd = f"rename --name {src} --title {dst}"
        return self.execute(cmd)

    def set_window(self, name, w, h, dpi, rotate=1, lockwindow=0):
        cmd = f"modify --name {name} --resolution {w},{h},{dpi} --autorotate {rotate} --lockwindow {lockwindow}"
        return self.execute(cmd)

    def set_cpu(self, name, count):
        cmd = f"modify --name {name} --cpu {count}"
        return self.execute(cmd)

    def set_memory(self, name, size):
        cmd = f"modify --name {name} --memory {size}"
        return self.execute(cmd)

    def set_root(self, name, state):
        cmd = f"modify --name {name} --root {state}"
        return self.execute(cmd)

    def set_mac(self, name, mac):
        cmd = f"modify --name {name} --mac {mac}"
        return self.execute(cmd)

    def set_factory(self, name, manufacturer, model, pnumber, imei, imsi, simserial, androidid):
        cmd = f"modify --name {name} --manufacturer {manufacturer} " \
              f"--model {model} " \
              f"--pnumber {pnumber} " \
              f"--imei {imei} " \
              f"--imsi {imsi} " \
              f"--simserial {simserial} " \
              f"--androidid {androidid} "
        return self.execute(cmd)

    def get_device(self, name):
        """
        获取 adb 连接需要的 驱动
        :return:
        """
        cmd = f"adb --name {name}  --command devices -l"
        return self.execute(cmd).strip().split("\n")[self._get_index(name) + 1].split()[0]

    def _get_index(self, name):
        return int({x["name"]: x["index"] for x in self.list()}[name])

    def input(self, name, text):
        cmd = f"action --name {name} --key call.input --value \"{text}\""
        return self.execute(cmd)
