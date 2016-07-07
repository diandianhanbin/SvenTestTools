# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com
import os
import sys
import adbconfig


class Adb(object):
	def __init__(self):
		self.checkconnect = adbconfig.COMMAND['checkConnect']
		self.thirdpackage = adbconfig.COMMAND['thirdpackage']
		self.curpknm = adbconfig.COMMAND['getcurpknm']

	def checkConnect(self):
		"""
		检查设备的连接状态
		:return: True or False
		"""
		deviceList = self.anafile(os.popen(self.checkconnect))
		status = True if len(deviceList) > 2 else False
		return status

	def anafile(self, fileobj):
		"""
		返回对象所有的列,以列表形式返回
		:param fileobj:对象
		:return:List, 去空格的列表
		"""
		data = [x.strip() for x in fileobj]
		return data

	def getDevicesName(self):
		"""
		获取设备名称
		:return:设备名称
		"""
		data = {}
		a = os.popen('adb devices')
		devices = a.readlines()
		spl = devices[1].find('	')
		devices_name = devices[1][:spl]
		if devices_name == '':
			data['status'] = "ERROR"
			data['msg'] = "请确认设备是否连接"
			return data
		else:
			data['status'] = "OK"
			data['msg'] = devices_name
			return data

	def getThirdPackage(self):
		"""
		获取手机中的第三方应用名称
		:return:
		"""
		if not self.checkConnect():
			pk_data = {
				"status": "ERROR",
				"msg": "请检查设备是否正确连接"
			}
			return pk_data
		f = self.anafile(os.popen(self.thirdpackage))
		thirdNames = [x.strip().split(":")[1] for x in f]
		data = {
			"status": "OK",
			"msg": "查询成功",
			"thirdNames": thirdNames
		}
		return data

	def getCurPknm(self):
		"""
		获取手机当前运行的程序包名和Activity名
		:return:包名和Activity名
		"""
		if not self.checkConnect():
			pk_data = {
				"status": "ERROR",
				"msg": "请检查设备是否正确连接"
			}
			return pk_data
		f = self.anafile(os.popen(self.curpknm))
		pknm = [x.strip().split(" ")[4] for x in f]

		pk_info = pknm[0].split('/')
		pk_data = {
			'msg': '查询成功',
			'status': "OK",
			'package_name': pk_info[0],
			'activity_name': pk_info[1].rstrip("}")
		}
		return pk_data


class BatteryInfo(Adb):
	def __init__(self):
		Adb.__init__(self)
		self.getbatteryinfo = adbconfig.COMMAND['getBattery']

	def getBatteryInfo(self):
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
		if not self.checkConnect():
			rst_data['msg'] = "未检测到设备,请检查设备是否正确连接"
			rst_data['status'] = "ERROR"
			return rst_data

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
	ad = Adb()
	# print ad.checkConnect()
	print ad.getThirdPackage()
	# bat = BatteryInfo()
	# print bat.getBatteryInfo()
	# cpu = CpuInfo()
	# print cpu.getCPUInfo()
	# mem = MemInfo()
	# mem.getMemInfo()
	# baseinfo = BaseInfo()
	# baseinfo.getBaseInfo()