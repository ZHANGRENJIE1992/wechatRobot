import pymysql
# 打开数据库连接
import shortuuid

def createuuid():
	return shortuuid.uuid()


class db(object):
	def __init__(self):
		self.get_conn()
	# 打开数据库连接
	def get_conn(self):
		try:
			self.a = 1
			self.conn = pymysql.connect(
				host='127.0.0.1',
				port=3306,
				user='root',
				password='ZRJ19920708',
				charset='utf8',
				database='itchat'
				#,
				#cursor=pymysql.cursors.DictCursor
			)
		except db.Error as e:
			print(e+"connection failed")

 	#关闭数据库连接
	def close_conn(self):
		try:
			if self.conn:
				self.conn.close()
		except pymysql.Error as e:
			print(e,"close failed")
	#添加数据
	def create_data(self,wechatid,content,time,groupid,groupsize):
		try:
			#创建sql
			sql = ("INSERT INTO `CHAT_CONTENT`(`uuid`,`WechatID`,`Content`,`Time`,`GroupName`,`GroupSize`) VALUES"
                    "(%s,%s,%s,%s,%s,%s);")
			#获取cusor
			cursor = self.conn.cursor()
			#执行sql
			contentid = createuuid()
			cursor.execute(sql,(contentid,wechatid,content,time,groupid,groupsize))
			#提交事物
			self.conn.commit()

		except pymysql.Error as e:
			print(e, "close failed")
			#print('error')
			self.conn.commit()   # 如果上面的提交有错误，那么只执行对的那一个提交

		# 关闭连接
		cursor.close()
		self.close_conn()
	

	def get_dailyinfo(self,year,month,day):
		#创建sql

		sql = ('SELECT ct.* FROM CHAT_CONTENT AS ct WHERE YEAR(ct.Time) = %s AND MONTH(ct.Time) = %s AND DAY(ct.Time) = %s ORDER BY ct.uuid DESC ;')
		# 获取cursor

		cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
		# 执行sql
		cursor.execute(sql,[year,month,day])
		a = cursor.fetchall()
		
		# 关闭连接
		cursor.close()
		self.close_conn()

		return a




#def main():
#	sql = db()
	# sql.get_more(3,2)
	#sql.create_data(contentid=1,wechatid='111',content="第一句话",time="20191220000000",groupid=111,groupsize=4)
	#sql.create_data(2,'M112',"第一句话","20191221100000",1111,6)
#	sql.get_dailyinfo()
 
#if __name__ == '__main__':
#	main()



# 使用 cursor() 方法创建一个游标对象 cursor
#cursor = db.cursor()

 # 使用预处理语句创建表

#sql = """
#CREATE TABLE CHAT_CONTENT(
#id       INT auto_increment PRIMARY KEY ,
#WechatID CHAR(30) NOT NULL,
#Content  TEXT,
#Time     TIMESTAMP,
#GroupName INT, 
#GroupSize INT
#)ENGINE=innodb DEFAULT CHARSET=utf8;"""
# 使用 execute() 方法执行 SQL，如果表存在则删除

#cursor.execute(sql)
 
# 关闭数据库连接
#db.close()