# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com
import os
import sys
import adbconfig


class Adb(object):
	def __init__(self):
		self.checkconnect = adbconfig.COMMAND['checkConnect']

	def checkConnect(self):
		deviceList = self.anafile(os.popen(self.checkconnect))
		status = True if len(deviceList) > 2 else False
		return status

	def anafile(self, fileobj):
		data = [x.strip() for x in fileobj]
		return data


class BatteryInfo(Adb):
	def __init__(self):
		Adb.__init__(self)
		self.getbatteryinfo = adbconfig.COMMAND['getBattery']

	def getBatteryInfo(self):
		data = []
		Batteryinfo = self.anafile(os.popen(self.getbatteryinfo))
		data = [
			'电源供电(AC powered): {}'.format(Batteryinfo[1].split(":")[1]),
			"USB供电(USB powered: {}".format(Batteryinfo[2].split(":")[1]),
			"当前电量(level): {}%".format(Batteryinfo[7].split(":")[1]),
			"电池温度(temperature: {}°".format(str(float(Batteryinfo[10].split(":")[1])/10)),
			"电池类型(technology): {}".format(Batteryinfo[11].split(":")[1])
		]
		return data


class CpuInfo(Adb):
	def __init__(self):
		Adb.__init__(self)
		self.getcpuinfo = adbconfig.COMMAND['cpuinfo']

	def getCPUInfo(self):
		CPUInfo = self.anafile(os.popen(self.getcpuinfo))
		data = [x for x in CPUInfo]
		return data


class MemInfo(Adb):
	def __init__(self):
		Adb.__init__(self)
		self.getmeminfo = adbconfig.COMMAND['meminfo']

	def getMemInfo(self):
		data = [
			"总内存(MemTotal): {} ".format(self.anafile((os.popen(self.getmeminfo+"|grep MemTotal")))[0].split(":")[1].strip()),
			"空余内存(MemFree): {}".format(self.anafile((os.popen(self.getmeminfo+"|grep MemFree")))[0].split(":")[1].strip()),
			"缓冲区内存(Buffers): {}".format(self.anafile((os.popen(self.getmeminfo+"|grep Buffers")))[0].split(":")[1].strip()),
			"活跃内存(Active): {}".format(self.anafile((os.popen(self.getmeminfo+"|grep Active")))[0].split(":")[1].strip()),
			"不活跃内存(Inactive): {}".format(self.anafile((os.popen(self.getmeminfo+"|grep Inactive")))[0].split(":")[1].strip())
		]
		return data


class BaseInfo(Adb):
	def __init__(self):
		Adb.__init__(self)
		self.getmobilemodel = adbconfig.COMMAND['mobilemodel']
		self.getmobilecpu = adbconfig.COMMAND['mobilecpu']
		self.getmobilemem = adbconfig.COMMAND['mobilemem']
		self.getdisplay = adbconfig.COMMAND['mobiledilplay']
		self.getsystemversion = adbconfig.COMMAND['mobileversion']
		self.getmobileimme = adbconfig.COMMAND['mobileimme']

	def getBaseInfo(self):
		data = [
			"手机型号: {}".format(self.anafile(os.popen(self.getmobilemodel))[0].split("=")[1].strip()),
			"处理器: {}".format(self.anafile(os.popen(self.getmobilecpu))[0].split(":")[1].strip()),
			"内存: {}".format(self.anafile(os.popen(self.getmobilemem))[0].split(":")[1].strip()),
			"屏幕分辨率: {}".format(self.anafile(os.popen(self.getdisplay))[0][17:].split(",")[0].split(":")[1].strip()),
			"系统版本: {}".format(self.anafile(os.popen(self.getsystemversion))[0]),
			"手机串号: {}".format(self.anafile(os.popen(self.getmobileimme))[0].split("=")[1].strip())
		]
		return data


class CommonFunction(Adb):
	def __init__(self):
		Adb.__init__(self)
		self.installCommand = adbconfig.COMMAND['install']

	def install(self, iscovered, apkaddress):
		rst_data = {}
		if iscovered == u"true":
			command = adbconfig.COMMAND['install']+"-r "+apkaddress
			os.system(command.encode('utf-8'))
			rst_data['msg'] = "安装完毕"
			rst_data['status'] = "OK"

		elif iscovered == u"false":
			command = adbconfig.COMMAND['install'] + apkaddress
			status = self.anafile(os.popen(command.encode('utf-8')))
			for x in status:
				if "Failure" in x:
					rst_data['msg'] = "安装失败,手机中已存在该APP,请使用覆盖安装"
					rst_data['status'] = "ERROR"
					return rst_data
			rst_data['msg'] = "安装完毕"
			rst_data['status'] = "OK"

		else:
			rst_data['msg'] = "未知错误,安装失败"
			rst_data['status'] = "ERROR"

		return rst_data


if __name__ == '__main__':
	# ad = Adb()
	# print ad.checkConnect()
	# bat = BatteryInfo()
	# print bat.getBatteryInfo()
	# cpu = CpuInfo()
	# print cpu.getCPUInfo()
	# mem = MemInfo()
	# mem.getMemInfo()
	baseinfo = BaseInfo()
	baseinfo.getBaseInfo()