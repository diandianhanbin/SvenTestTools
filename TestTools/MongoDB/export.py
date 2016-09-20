# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com
import csv
import time
import xlwt
import sys
sys.path.append("..")

import mongodb
import common

class Export(object):
	def __init__(self):
		self.mdb = mongodb.MongoDB()
		self.collection = 'bugContent'
		self.cm = common.Common()
		self.titles = [u'缺陷编号', u'缺陷标题', u'缺陷描述', u'重现步骤', u'缺陷状态',u'所属终端', u'所属项目', u'开发人员', u'测试人员', u'创建日期']

	def getSingleBugContent(self, bugID):
		queryConditions = {
			'bugID': bugID
		}
		bugContent = self.mdb.dbQueryOneRecord(self.collection, **queryConditions)
		return bugContent

	def exportExcel(self, bugIDs):
		print bugIDs
		workbook = xlwt.Workbook()
		sheet = workbook.add_sheet(u"缺陷导出表")
		bond_style = xlwt.easyxf('font: bold 1')
		for i, x in enumerate(self.titles):
			sheet.write(0, i, x, bond_style)
		for i, x in enumerate(bugIDs):
			bug = [
				self.getSingleBugContent(int(x))['bugID'],
				self.getSingleBugContent(int(x))['bugTitle'],
				self.getSingleBugContent(int(x))['bugDescription'],
				self.getSingleBugContent(int(x))['bugStep'],
				self.cm.changeBugStatus(self.getSingleBugContent(int(x))['bugStatus']),
				self.getSingleBugContent(int(x))['Terminal'],
				self.getSingleBugContent(int(x))['Project'],
				self.getSingleBugContent(int(x))['Developer'],
				self.getSingleBugContent(int(x))['Tester'],
				self.getSingleBugContent(int(x))['Date']
			]
			for n, y in enumerate(bug):
				sheet.write(i+1, n, y)
		workbook.save("缺陷导出表.xls")

	def exportCSV(self):
		pass

	def exportTXT(self):
		pass

	def exportJSON(self):
		pass

	def exportHTML(self):
		pass

if __name__ == '__main__':
	export = Export()
	print export.getSingleBugContent(11)
	export.exportExcel([11, 12])