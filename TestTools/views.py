# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com

from django.shortcuts import render
from MongoDB import config, mongodb, export
import time
from django.http import JsonResponse
import requests
from mobile import adb
mdb = mongodb.MongoDB()


def index(request):
	return render(request, 'TestTools/index.html')


def bugrecord(request):
	projcet_rst = mdb.dbQueryAllRecord(config.COLLECTION['project'])
	project = [x['name'] for x in projcet_rst]
	bugStatus_rst = mdb.dbQueryAllRecord(config.COLLECTION['bugStatus'])
	bugStatus = []
	for x in bugStatus_rst:
		data = {
			"name": x['status'],
			"code": x['code']
		}
		bugStatus.append(data)
	bugStatusCount = [mdb.dbQueryCount(config.COLLECTION['bugContent'], **{"bugStatus": "1"}),
					  mdb.dbQueryCount(config.COLLECTION['bugContent'], **{"bugStatus": "2"}),
					  mdb.dbQueryCount(config.COLLECTION['bugContent'], **{"bugStatus": "3"}),
					  mdb.dbQueryCount(config.COLLECTION['bugContent'], **{"bugStatus": "4"})]

	return render(request, 'TestTools/bugrecord.html', {"project": project,
														"bugStatus": bugStatus,
														"bugStatusCount": bugStatusCount})


def newbug(request, bugtype, bugid):
	if bugtype == "new":
		newid = 0
		if request.method == 'POST':
			data = {
				"Project": request.POST['Project'],
				"bugTitle": request.POST['bugTitle'],
				"Terminal": request.POST['Terminal'],
				"bugDescription": request.POST['bugDescription'],
				"bugStep": request.POST['bugStep'],
				"Developer": request.POST['Developer'],
				"Tester": request.POST['Tester'],
				"bugStatus": request.POST['bugStatus'],
				"bugID": mdb.getBugID(),
				"Date": time.strftime('%Y%m%d')
			}
			mdb.dbInsertOneRecord(config.COLLECTION['bugContent'], **data)
			mdb.bugPlus()
			newid = mdb.getBugID()-1
		return render(request, 'TestTools/newbug.html', {"type": "new", "newid": newid})
	elif bugtype == "update":
		return render(request, 'TestTools/newbug.html', {"type": "update", "bugID": bugid})
	return render(request, 'TestTools/newbug.html')


def bugdetail(request, bugid):
	record = mdb.dbQueryOneRecord(config.COLLECTION['bugContent'], **{"bugID": int(bugid)})
	if record is not None:
		rst_data = {
			"Project": record['Project'],
			"Tester": config.TESTER[record['Tester']][1],
			"bugStep": record['bugStep'],
			"Terminal": config.TERMINAL[record['Terminal']][1],
			"bugID": record['bugID'],
			"bugStatus": config.BUGSTATUS[record['bugStatus']][1],
			"Date": record['Date'],
			"bugDescription": record['bugDescription'],
			"bugTitle": record['bugTitle'],
			"Developer": config.DEVELOPER[record['Developer']][1],
		}
		return render(request, 'TestTools/bugdetail.html', {"record": rst_data, "errmsg": "True"})
	else:
		return render(request, 'TestTools/bugdetail.html', {"errmsg": "False"})


def updateBugContent(request, bugid):
	if request.method == "POST":
		data = {
			"Project": request.POST['Project'],
			"bugTitle": request.POST['bugTitle'],
			"Terminal": request.POST['Terminal'],
			"bugDescription": request.POST['bugDescription'],
			"bugStep": request.POST['bugStep'],
			"Developer": request.POST['Developer'],
			"Tester": request.POST['Tester'],
			"bugStatus": request.POST['bugStatus'],
		}

		mdb.dbUpdateOneRecord(config.COLLECTION['bugContent'], [data, {"bugID": int(bugid)}])
		return bugdetail(request, bugid)


def newproject(request):
	"""
	新建项目
	:return: None
	"""
	if request.method == "POST":
		data = {
			"name": request.POST['project']
		}
		if mdb.dbInsertOneRecord(config.COLLECTION['project'], **data):
			return render(request, 'TestTools/newproject.html', {"errmsg": "True"})
		else:
			return render(request, 'TestTools/newproject.html', {"errmsg": "False"})

	return render(request, 'TestTools/newproject.html', {"errmsg": "None"})


def idcardquery(request):
	"""
	生成身份证
	:return: None
	"""
	if request.method == "POST":
		url = 'http://identity.daoapp.io/api'
		payload = {
			"num": request.POST['num']
		}
		r = requests.get(url, params=payload)
		print r.url
		jsonData = r.json()
		print jsonData
		return render(request, 'TestTools/shenfenzhengshengcheng/shenfenzheng.html', {"iddata": jsonData})
	return render(request, 'TestTools/shenfenzhengshengcheng/shenfenzheng.html')


# =========================================Mobile==================================================

def baseinfo(request):
	return render(request, 'TestTools/mobileTest/baseinfo.html')


def commonfunction(request):
	return render(request, 'TestTools/mobileTest/commonfunction.html')


def checkinfo(request):
	return render(request, 'TestTools/mobileTest/checkinfo.html')


# =========================================Ajax==================================================
# =========================================Ajax==================================================

def getAllBug(request):
	"""
	获取所有bug的数据
	:param request:
	:return:
	"""
	bugContent = mdb.dbQueryAllRecord(config.COLLECTION['bugContent'])
	rst_data = []
	for x in bugContent:
		bug_data = {
			"ID": x['bugID'],
			"Status": x['bugStatus'],
			"Tester": x['Tester'],
			"Date": x['Date'],
			"BugStep": x['bugStep'],
			"Terminal": config.TERMINAL[x['Terminal']][1],
			"BugDescription": x['bugDescription'],
			"BugTitle": x['bugTitle'],
			"Developer": config.DEVELOPER[x['Developer']][1],
			"Project": x['Project']
		}
		rst_data.append(bug_data)
	rst_data = rst_data[::-1]
	return JsonResponse(rst_data, safe=False)


def getNewBugElements(request):
	"""
	获取新bug的元素
	:param request:
	:return:
	"""
	project_query = mdb.dbQueryAllRecord(config.COLLECTION['project'])
	project_name = [x['name'] for x in project_query]
	rst_data = {
		"developer": config.DEVELOPER.values(),
		"tester": config.TESTER.values(),
		"terminal": config.TERMINAL.values(),
		"bugstatus": config.BUGSTATUS.values(),
		"project": project_name
	}
	return JsonResponse(rst_data, safe=False)


def getOneBugElement(request, bugid):
	"""
	根据bugid获取bug内容
	:param request:
	:param bugid: bugid
	:return:
	"""
	bugRecord = mdb.dbQueryOneRecord(config.COLLECTION['bugContent'], **{"bugID": int(bugid)})
	bug_data = {
		"ID": bugRecord['bugID'],
		"Status": bugRecord['bugStatus'],
		"Tester": bugRecord['Tester'],
		"Date": bugRecord['Date'],
		"BugStep": bugRecord['bugStep'],
		"Terminal": config.TERMINAL[bugRecord['Terminal']][1],
		"BugDescription": bugRecord['bugDescription'],
		"BugTitle": bugRecord['bugTitle'],
		"Developer": config.DEVELOPER[bugRecord['Developer']][1],
		"Project": bugRecord['Project']
	}
	return JsonResponse(bug_data, safe=False)


def getBugAccordingToCondition(request):
	"""
	根据某种条件来获取bug记录
	:param request:
	:param kwargs:查询条件
	:return:
	"""
	queryData = dict()
	try:
		bugStatus = request.GET.get("BugStatus")[::-1][0]  # 从id中获取status
		queryData['bugStatus'] = bugStatus
	except:
		bugStatus = ""
	try:
		project = request.GET.get("Project")
		queryData['Project'] = project
	except:
		project = ""
	bugRecord = mdb.dbQueryCondition(config.COLLECTION['bugContent'], **queryData)
	rst_data = []
	for x in bugRecord:
		bug_data = {
			"ID": x['bugID'],
			"Status": x['bugStatus'],
			"Tester": x['Tester'],
			"Date": x['Date'],
			"BugStep": x['bugStep'],
			"Terminal": config.TERMINAL[x['Terminal']][1],
			"BugDescription": x['bugDescription'],
			"BugTitle": x['bugTitle'],
			"Developer": config.DEVELOPER[x['Developer']][1],
			"Project": x['Project']
		}
		rst_data.append(bug_data)
	rst_data = rst_data[::-1]
	return JsonResponse(rst_data, safe=False)


def getAndroidInfo(request):
	BatteryInfo = adb.BatteryInfo().getBatteryInfo()
	CPUInfo = adb.CpuInfo().getCPUInfo()
	MemInfo = adb.MemInfo().getMemInfo()
	BaseInfo = adb.BaseInfo().getBaseInfo()
	rst_data = {
		"cpuinfo": CPUInfo,
		"meminfo": MemInfo,
		"batteryinfo": BatteryInfo,
		"baseinfo": BaseInfo,
	}
	return JsonResponse(rst_data, safe=False)


def apkInstall(request):
	iscovered = request.GET.get('iscovered')
	apkaddress = request.GET.get('apkaddress')
	data = adb.CommonFunction().install(iscovered, apkaddress)
	return JsonResponse(data, safe=False)


def getCurPknm(request):
	data = adb.Adb().getCurPknm()
	return JsonResponse(data, safe=False)


def getThirdPknm(request):
	data = adb.Adb().getThirdPackage()
	return JsonResponse(data, safe=False)


def checkAndroidInfo(request):
	pass


def exportBug(request):
	"""
	导出不同格式的缺陷记录
	:param request: 使用request.Get.get()方法获取参数"exporttype"和"bugids[]"
	:return:
	"""
	exporttype = request.GET.get("exporttype")
	bugids = request.GET.getlist("bugids[]")
	ep = export.Export()
	if exporttype == 'Excel':
		try:
			ep.exportExcel(bugids)
			errstatus = 'OK'
			errmsg = '导出成功'
		except Exception as e:
			errstatus = 'ERROR'
			errmsg = e
	elif exporttype == "HTML":
		try:
			ep.exportHTML(bugids)
			errstatus = 'OK'
			errmsg = '导出成功'
		except Exception as e:
			errstatus = 'ERROR'
			errmsg = e
	else:
		errstatus = 'ERROR'
		errmsg = '传入的导出方式不正确'
	rst_data = {
		"exportType": str(exporttype),
		"errstatus": errstatus,
		"errmsg": errmsg
	}
	return JsonResponse(rst_data, safe=False)


def downloadBug(request):
	pass


def kxiantu(request):
	return render(request, 'TestTools/kxiantu.html')


def getCharts(request):
	dates = []
	series = []
	echartSeries = []
	Project = request.GET.get('project')
	queryData = {"project": Project}
	bugArchives = mdb.dbQueryCondition('bugArchive', **queryData)
	for x in bugArchives:
		sery = {
			"yiyanzheng": x['yiyanzheng'],
			"weijiejue": x['weijiejue'],
			"yixiufu": x['yixiufu'],
			"feiwenti": x['feiwenti'],
			"date": x['date']
		}
		dates.append(x['date'])
		series.append(sery)

	data_weijiejue = {
		'name': "未解决",
		"type": "line",
		"areaStyle": "{normal: {}}",
		"data": [x['weijiejue'] for x in series]
	}

	data_yijiejue = {
		"name": "已修复",
		"type": "line",
		"areaStyle": "{normal: {}}",
		"data": [x['yixiufu'] for x in series]
	}

	data_yiyanzheng = {
		"name": "已验证",
		"type": "line",
		"areaStyle": "{normal: {}}",
		"data": [x['yiyanzheng'] for x in series]
	}

	data_feiwenti = {
		"name": "非问题",
		"type": "line",
		"areaStyle": "{normal: {}}",
		"data": [x['feiwenti'] for x in series]
	}
	echartSeries.append(data_weijiejue)
	echartSeries.append(data_yijiejue)
	echartSeries.append(data_yiyanzheng)
	echartSeries.append(data_feiwenti)

	rstData = {
		'dates': dates,
		"series": series,
		'projectName': Project,
		'EchartData': echartSeries
	}

	return JsonResponse(rstData, safe=False)
