# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com
import pymongo
import config
import json
from bson.json_util import dumps

post = {"bugStatus": "1"}
# newpost = "{'Project': u'\u5fae\u8bc1\u5238APP', 'Terminal': u'web', 'bugStatus': u'1', 'Tester': u'wengyb', 'bugDescription': u'testsdgsdgsdgsdfgsdfgsdfg', 'Developer': u'xucx', 'bugTitle': u'testsdgsdgsdg', 'bugStep': u'testsdgsdgsg'}"
# post = {
# 	"bugID": 2,
# 	"Terminal": "IOS",
# 	"bugTitle": "不会在通知栏提醒消息、在我的消息中也没有记录",
# 	"bugDescription": "缺陷描述",
# 	"bugStep": "1、搜索一直未在自选列表的股票.2、做下角不应该显示为“更多”而是添加自选",
# 	"Developer": "李小斌",
# 	"Tester": "翁彦彬",
# 	"Date": "20160613",
# 	"Status": "1",
# 	"Project": "微证券APP"
# }


class MongoDB(object):
	def __init__(self):
		try:
			self.client = pymongo.MongoClient()
			self.datebase = self.client[config.DB['datebase']]
		except:
			print 'datebase connect error'

	def __chooseCollection(self, collection):
		"""
		选择数据库中的集合
		:param collection:集合的名称
		:return:集合的句柄
		"""
		db_collection = self.datebase[collection]
		return db_collection

# ===================新增操作===============================
	def dbInsertOneRecord(self, collection, **kwargs):
		"""
		添加一条数据到数据
		:param collection:集合的名称
		:param kwargs: 数据内容
		:return:True or False
		"""
		dbinsert = self.__chooseCollection(collection)
		try:
			dbinsert.insert_one(kwargs)
			return True
		except:
			print 'insert {} error'.format(collection)
			return False

# ===================查询操作===============================
	def dbQueryOneRecord(self, collection, **kwargs):
		"""
		查询一条数据
		:param collection:集合的名称
		:param kwargs: 查询的条件,为空则查询第一条
		:return:查询的结果
		"""
		dbquery = self.__chooseCollection(collection)
		rst = dbquery.find_one(kwargs)
		return rst

	def dbQueryAllRecord(self, collection):
		"""
		查询所有数据
		:param collection:集合的名称
		:return: 查询的结果
		"""
		dbquery = self.__chooseCollection(collection)
		record = dbquery.find()
		return record

	def dbQueryCondition(self, collection, **kwargs):
		"""
		根据条件查询数据
		:param collection:集合的名称
		:param kwargs: 条件
		:return:查询的结果
		"""
		dbquery = self.__chooseCollection(collection)
		record = dbquery.find(kwargs)
		return record

	def dbQueryCount(self, collection, **kwargs):
		"""
		根据条件查询数据记录数
		:param collection:集合的名称
		:param kwargs:条件
		:return:查询的结果
		"""
		dbquery = self.__chooseCollection(collection)
		count = dbquery.find(kwargs).count()
		return count

# ===================删除操作===============================
	def dbDeleteOneRecord(self, collection, **kwargs):
		"""
		删除一条数据
		:param collection:集合的名称
		:param kwargs: 删除数据的条件
		:return:None
		"""
		dbdelete = self.__chooseCollection(collection)
		try:
			dbdelete.delete_one(kwargs)
		except:
			print 'delete {} error'.format(collection)

# ===================更新操作===============================
	def dbUpdateOneRecord(self, collection, uplist):
		"""
		对数据库更新一条记录
		:param collection:数据库的集合
		:param uplist: 更新的字段[查询的条件, 更新的数据]
		:return:
		"""
		dbupdate = self.__chooseCollection(collection)
		condition = uplist[0]
		new_data = uplist[1]
		try:
			dbupdate.update_one(new_data, {"$set": condition})
			return True
		except:
			print 'update {} error'.format(collection)
			return False

# ===================数据库自增字段操作===============================
	def getBugID(self):
		"""
		获取当前bug的最新编号
		:return:bugID
		"""
		db = self.__chooseCollection(config.COLLECTION['bugID'])
		rst = db.find_one()
		return rst['bugID']

	def bugPlus(self):
		"""
		bugID自增
		:return:True
		"""
		db = self.__chooseCollection(config.COLLECTION['bugID'])
		db.update_one({"bugID": self.getBugID()}, {"$inc": {"bugID": 1}})
		return True

if __name__ == '__main__':
	mdb = MongoDB()
	# print mdb.dbQueryOneRecord(config.COLLECTION['category'])
	# mdb.dbInsertOneRecord(config.COLLECTION['bugContent'], **post)
	# mdb.dbDeleteOneRecord(config.COLLECTION['project'], **post)
	# mdb.dbUpdateOneRecord(config.COLLECTION['bugContent'], newpost, **post)
	# mdb.bugPlus()
	# print mdb.getBugID()
	# for x in mdb.dbQueryCondition(config.COLLECTION['bugContent'], **post):
	# 	print x
	print mdb.dbQueryCount(config.COLLECTION['bugContent'], **post)
