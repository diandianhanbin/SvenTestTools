# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com

from django.shortcuts import render
from mongodb import config, mongodb
import time
from django.http import JsonResponse
from django.http import HttpResponseRedirect

mdb = mongodb.MongoDB()


def index(request):
	return render(request, 'TestTools/index.html')


def mobile(request):
	return render(request, 'TestTools/mobile.html')


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
		return render(request, 'TestTools/newbug.html', {"type": "new"})
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
	if request.method == "POST":
		data = {
			"name": request.POST['project']
		}
		if mdb.dbInsertOneRecord(config.COLLECTION['project'], **data):
			return render(request, 'TestTools/newproject.html', {"errmsg": "True"})
		else:
			return render(request, 'TestTools/newproject.html', {"errmsg": "False"})

	return render(request, 'TestTools/newproject.html', {"errmsg": "None"})


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