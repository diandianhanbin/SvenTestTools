# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com

COMMAND = {
	"checkConnect": "adb devices",
	"getBattery": "adb shell dumpsys battery",
	"cpuinfo": "adb shell cat /proc/cpuinfo",
	"meminfo": "adb shell cat /proc/meminfo",
	"mobilemodel": "adb shell cat /system/build.prop | grep ro.product.model",
	"mobilecpu": "adb shell cat /proc/cpuinfo | grep Processor",
	"mobilemem": "adb shell cat /proc/meminfo | grep MemTotal",
	"mobiledilplay": "adb shell dumpsys display | grep DisplayDeviceInfo",
	"mobileversion": "adb shell getprop ro.build.version.release",
	"mobileimme": "adb shell dumpsys iphonesubinfo | grep Device",
}