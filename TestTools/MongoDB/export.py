# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com
import csv
import time
import xlwt
import sys
import requests
import os
import mongodb
import common
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append("..")

_htmlHeader = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>缺陷导出表</title>
    <link rel="stylesheet" href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css">
    <script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
    <script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>

<body>
    <div class="page-header">
        <h1>缺陷导出表 <small>点击缺陷编号查询详情</small></h1>
    </div>
    <table class="table table-striped">
        <thead>
            <tr>
                <th>编号</th>
                <th>终端</th>
                <th>标题</th>
                <th>开发人员</th>
                <th>缺陷状态</th>
            </tr>
        </thead>
        <tbody>
"""

_htmlFooter = """
</tbody>
    </table>
</body>
</html>
"""


class Export(object):
	def __init__(self):
		self.mdb = mongodb.MongoDB()
		self.collection = 'bugContent'
		self.cm = common.Common()
		self.titles = [u'缺陷编号', u'缺陷标题', u'缺陷描述', u'重现步骤', u'缺陷状态', u'所属终端', u'所属项目', u'开发人员', u'测试人员', u'创建日期']

	def getSingleBugContent(self, bugID):
		"""
		获取单个bug的内容
		:param bugID: int, BugID
		:return:dict, bug内容

		返回字段说明:
		bugID: 缺陷编号
		bugTitle: 缺陷标题
		bugDescription: 缺陷描述
		bugStep: 缺陷步骤
		bugStatus: 缺陷状态
		Terminal: 缺陷所属终端
		Project: 所属项目
		Developer: 开发人员
		Tester: 测试人员
		Date: 日期
		"""
		queryConditions = {
			'bugID': bugID
		}
		bugContent = self.mdb.dbQueryOneRecord(self.collection, **queryConditions)
		return bugContent

	def exportExcel(self, bugIDs):
		"""
		根据传入的bug编号导出Excel格式的bug记录
		:param bugIDs:list, bug编号的列表
		:return: None
		"""
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
				sheet.write(i + 1, n, y)
		workbook.save("缺陷导出表.xls")

	def exportCSV(self):
		pass

	def exportTXT(self):
		pass

	def exportJSON(self):
		pass

	def exportHTML(self, bugIDs):
		"""
		根据传入的bug编号导出HTML格式的bug记录
		:param bugIDs:list, bug编号的列表
		:return: None
		"""
		header = _htmlHeader
		footer = _htmlFooter
		bodys = []
		for x in bugIDs:
			htmlbodyer = "<tr><td><a href='htmlBugDetails/{0}.html'>{0}</a></td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td></tr>".format(
				self.getSingleBugContent(int(x))['bugID'],
				self.getSingleBugContent(int(x))['Terminal'],
				self.getSingleBugContent(int(x))['bugTitle'],
				self.cm.changeDevelopName(self.getSingleBugContent(int(x))['Developer']),
				self.cm.changeBugStatus(self.getSingleBugContent(int(x))['bugStatus'])
			)
			bodys.append(htmlbodyer)
		with open('index.html', 'w') as f:
			f.write(header)
			f.write(''.join(bodys))
			f.write(footer)
		self.getHTMLDetail(bugIDs)

	def getHTMLDetail(self, bugIDs):
		"""
		根据传入的bugID来获取网页的详细内容
		:param bugIDs: list, bug编号的列表
		:return: None
		"""
		self.cleanHTML()
		_url = 'http://localhost:2222/testtools/bugdetail/'
		for x in bugIDs:
			r = requests.get(_url+str(x)+"/")
			with open('htmlBugDetails/{}.html'.format(str(x)), 'w') as f:
				f.write(r.text)

	def cleanHTML(self):
		"""
		清除文档中的所有html记录
		:return:None
		"""
		add = '/Users/SvenWeng/PycharmProjects/SvenTestTools/htmlBugDetails/'
		htmls = os.listdir(add)
		if len(htmls) != 0:
			for x in htmls:
				os.remove(add+x)


if __name__ == '__main__':
	export = Export()
	# print export.getSingleBugContent(11)
	# export.exportExcel([11, 12])
	# export.getHTMLDetail([11, 12])
	export.cleanHTML()