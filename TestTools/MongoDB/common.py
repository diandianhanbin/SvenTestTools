# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com


class Common(object):
	def __init__(self):
		pass

	def changeDevelopName(self, name):
		pass

	def changeBugStatus(self, status):
		if status == '1':
			return u'未解决'
		elif status == '2':
			return u'已修复'
		elif status == '3':
			return u'已验证'
		elif status == '4':
			return u'非问题'
		else:
			return u'未知状态'
