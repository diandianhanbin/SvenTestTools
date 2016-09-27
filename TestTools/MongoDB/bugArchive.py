# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com
import mongodb
import time

mdb = mongodb.MongoDB()


def getProjectName():
	"""
	返回所有项目名称
	:return: List, 项目名称
	"""
	projectObj = mdb.dbQueryAllRecord('project')
	projects = [x['name'] for x in projectObj]
	return projects


def getBugStatus(projectName):
	"""
	根据项目名称按照日期归档bug数量
	:param projectName: str, 项目名称
	:return:
	"""
	weijiejue = 0
	yixiufu = 0
	yiyanzheng = 0
	feiwenti = 0
	bugs = mdb.dbQueryCondition('bugContent', **{'Project': projectName})
	for x in bugs:
		if x['bugStatus'] == '1':
			weijiejue += 1
		elif x['bugStatus'] == '2':
			yiyanzheng += 1
		elif x['bugStatus'] == '3':
			yixiufu += 1
		elif x['bugStatus'] == '4':
			feiwenti += 1
	Date = time.strftime('%Y%m%d')
	archiveDate = {
		'weijiejue': weijiejue,
		'yixiufu': yixiufu,
		'yiyanzheng': yiyanzheng,
		'feiwenti': feiwenti,
		'date': Date,
		'project': projectName
	}
	mdb.dbInsertOneRecord('bugArchive', **archiveDate)


def checkDateIsExist():
	"""
	检查当天是否有归档数据
	:return:Boolen,True表示当天无归档数据,False表示当天有归档数据
	"""
	status = mdb.dbQueryCount('bugArchive', **{'date': time.strftime('%Y%m%d')})
	if status == 0:
		return True
	else:
		return False


def runArchive():
	"""
	执行归档
	:return:None
	"""
	if checkDateIsExist():
		for x in getProjectName():
			try:
				getBugStatus(x)
			except Exception as e:
				print e
		print "{}数据归档完毕".format(time.strftime('%Y%m%d'))
	else:
		print '当天数据已归档'


if __name__ == '__main__':
	# getProjectName()
	# getBugStatus('股市直播')
	# checkDateIsExist()
	while 1:
		runArchive()
		time.sleep(3600)