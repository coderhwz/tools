#!/usr/bin/python2.7
#coding:utf-8
# 用于生成mysql数据库字段,使用于PHP的脚本，用法 fieldgenerate.py -d dbname -t tablename -m array|sql|attr
# 可以生成数组，属性和数据操作的列名部分，简单致极
# 需要安装 mysqldb库，pygtk(用于把生成的字符串放入剪切板)

import MySQLdb,getopt,sys,pygtk
pygtk.require('2.0')
import gtk

class Generator:

	con   = ''
	table = ''
	db    = ''
	mode  = 'array'
	user = 'hwz'
	pwd = 'who'
	host = '127.0.0.1'

	def printUsage(self):
		"""docstring for printUsage"""
		print 'Usage:\n -d for database name \n -t for table name \n -m for mode etc:attr,array,sql'

	def parseArgs(self,argv):
		"""docstring for parseArgs"""
		try:
			opts,args = getopt.getopt(argv[1:],"d:t:hh:m:")
		except Exception, e:
			self.printUsage()
			sys.exit(0)

		for key,value in opts:
			if	key == '-t':
				self.table = value

			if key == '-d':
				self.db = value

			if key == '-m':
				self.mode = value


	def initDb(self):
		"""docstring for in"""
		self.con = MySQLdb.connect(self.host,self.user,self.pwd,self.db) 
		
	def createSql(self,cursor):
		"""docstring for createSql"""
		string = ''
		for row in cursor.fetchall():
			string += self.table + '.' + row[0] + ', '
		return string

	def createAttr(self,cursor):
		"""docstring for createAttr"""
		string = ''
		for row in cursor.fetchall():
			string += '\tpublic $' + row[0] + ';\n'
		return string


	def createArray(self,cursor):
		"""docstring for fname"""
		string = '\t$'+self.table + ' = array(\n'
		for row in cursor.fetchall():
			string += '\t\t\'' + row[0] + '\'=>$' + row[0] + '\n'

		string += '\t);'
		return string
	
	def checkRequire(self):
		"""docstring for checkRequire"""
		if	self.table == '':
			print("table name is require!")
			sys.exit(0)

		if	self.db == '':
			print("db name is require!")
			sys.exit(0)

	def putInClipboard(self,string):
		"""docstring for putInClipboard"""
		clipboard = gtk.clipboard_get()
		clipboard.set_text(string)
		return clipboard.store()

	def main(self,argv):
		"""docstring for main"""
		self.parseArgs(argv)
		self.checkRequire()
		self.initDb()

		sql  = "desc " + self.table

		cursor = self.con.cursor()

		cursor.execute(sql)


		data = ''
		if	self.mode == 'array':
			data = self.createArray(cursor)

		if 	self.mode == 'sql':
			data = self.createSql(cursor)

		if	self.mode == 'attr':
			data =  self.createAttr(cursor)
		self.putInClipboard(data)

		print ("copied to clipboard")

generate = Generator()
generate.main(sys.argv)
