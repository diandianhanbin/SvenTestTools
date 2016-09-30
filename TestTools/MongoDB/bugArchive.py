# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com
import mongodb
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

mdb = mongodb.MongoDB()


def getProjectName():
	"""
	返回所有项目名称
	:return: List, 项目名称
	"""
	projectObj = mdb.dbQueryAllRecord('project')
	projects = [x['name'] for x in projectObj]
	return projects


def getBugStatus(projectName, archiveTime=time.strftime('%Y%m%d')):
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
			yixiufu += 1
		elif x['bugStatus'] == '3':
			yiyanzheng += 1
		elif x['bugStatus'] == '4':
			feiwenti += 1
	Date = archiveTime
	archiveDate = {
		'weijiejue': weijiejue,
		'yixiufu': yixiufu,
		'yiyanzheng': yiyanzheng,
		'feiwenti': feiwenti,
		'date': Date,
		'project': projectName
	}
	if archiveDate['weijiejue'] != 0:
		mdb.dbInsertOneRecord('bugArchive', **archiveDate)
		print '{}项目归档完毕'.format(archiveDate['project'])
	else:
		print '{}项目未解决问题为0,不执行归档'.format(archiveDate['project'])


def checkDateIsExist(archiveTime=time.strftime('%Y%m%d')):
	"""
	检查当天是否有归档数据
	:return:Boolen,True表示当天无归档数据,False表示当天有归档数据
	"""
	status = mdb.dbQueryCount('bugArchive', **{'date': archiveTime})
	if status == 0:
		return True
	else:
		return False


def runArchive(archiveTime=time.strftime('%Y%m%d')):
	"""
	执行归档
	:return:None
	"""
	if checkDateIsExist(archiveTime):
		for x in getProjectName():
			try:
				getBugStatus(x)
			except Exception as e:
				print e
		print "{}数据归档完毕".format(archiveTime)
	else:
		print '当天数据已归档'


if __name__ == '__main__':
	# getProjectName()
	# getBugStatus('股市直播')
	# checkDateIsExist()
	# while 1:
	# 	runArchive()
	# 	time.sleep(3600)
	# runArchive('20160927')
	while 1:
		if time.strftime('%H') == "17":
			runArchive()
		else:
			print '时间未到,不执行归档操作'
		time.sleep(3600)