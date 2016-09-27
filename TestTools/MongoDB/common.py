# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com


class Common(object):
	def __init__(self):
		pass

	def changeDevelopName(self, name):
		if name == 'ruanrj':
			return '阮荣军'
		elif name == 'lixb':
			return '李小斌'
		elif name == 'zhangsj':
			return '张帅军'
		elif name == 'xiongp':
			return '熊鹏'
		elif name == 'luoh':
			return '罗慧'
		elif name == 'xucx':
			return '徐成勋'
		elif name == 'wudw':
			return '吴道万'
		elif name == 'huangq':
			return '黄强'
		elif name == 'ios/android':
			return '李小斌/熊鹏'
		elif name == 'zhengzong':
			return '郑总'
		else:
			return '未知'


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
