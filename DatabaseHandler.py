import MySQLdb
import time

import datetime

"""
INSERT
UPDATE
DELETE
SELECT
"""
# HOST = "43.230.2.171"
HOST = "localhost"
# PORT = 9999
USER = "root"
PASSWD = "1234"
DB = "woongDB"

ERROR_MESSAGE = "DATABASE_ERROR"

class DatabaseHandler:
	def __init__(self):
		self.conn = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB)
		self.cursor = self.conn.cursor()
		self.cursor.execute("set names utf8;")

		'''
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS company(
			ID INT PRIMARY KEY AUTO_INCREMENT,
			name CHAR(20) NOT NULL,
			password CHAR(20) NOT NULL,
			phoneNumber CHAR(20),
			limitDate CHAR(20),
			signInDate CHAR(20))
			ENGINE=INNODB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_general_ci;
			""")
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS userInfo(
			ID INT PRIMARY KEY AUTO_INCREMENT,
			name CHAR(20) NOT NULL,
			socialNumber CHAR(20) NOT NULL,
			companyName CHAR(20) NOT NULL,
			phoneNumber CHAR(20),
			searchDate CHAR(20) NOT NULL)
			ENGINE=INNODB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_general_ci;
			""")
		'''

		self.conn.commit()

	def checkLogin(self, name, password):
		try:
			queryTemp = "SELECT EXISTS(SELECT * FROM company WHERE "
			queryTemp += "name='" + name + "' AND "
			queryTemp += "password='" + password + "')"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchone()
			if str(data[0]) == "1":
				return "TRUE"
			elif str(data[0]) == "0":
				return "FALSE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def getCompanyLimitDate(self, name):
		try:
			queryTemp = "SELECT limitDate FROM company WHERE "
			queryTemp += "name='" + name + "'"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchone()
			return data[0]
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def getCompanyPhoneNumber(self, name):
		try:
			queryTemp = "SELECT phoneNumber FROM company WHERE "
			queryTemp += "name='" + name + "'"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchone()
			return data[0]
		except Exception as e:
			print e
			return ERROR_MESSAGE

	# ADMIN_INSERT
	def checkCompanyNameExist(self, name):
		try:
			queryTemp = "SELECT EXISTS(SELECT * FROM company WHERE "
			queryTemp += "name='" + name + "')"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchone()
			if str(data[0]) == "1":
				return "TRUE"
			elif str(data[0]) == "0":
				return "FALSE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def insertCompany(self, name, password, phoneNumber):
		try:
			nowDate = datetime.date.today()
			queryTemp = "INSERT INTO company (name, password, phoneNumber, limitDate, signInDate) "
			queryTemp += "VALUES('" + name + "', "
			queryTemp += "'" + password + "', "
			queryTemp += "'" + phoneNumber + "', "
			queryTemp += "'" + nowDate.strftime("%Y-%m-%d") + "', "
			queryTemp += "'" + nowDate.strftime("%Y-%m-%d") + "')"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchone()
			return "TRUE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def updateCompanyLimitDate(self, name, limitDate):
		try:
			queryTemp = "UPDATE company SET limitDate=" + limitDate + " "
			queryTemp += "WHERE name='" + name + "'"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			return "TRUE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def checkUserInfoExist(self, name, socialNumber, companyName, phoneNumber, date):
		try:
			queryTemp = "SELECT EXISTS(SELECT * FROM userInfo WHERE "
			queryTemp += "name='" + userID + "' AND "
			queryTemp += "socialNumber='" + socialNumber + "' AND "
			queryTemp += "companyName='" + companyName + "' AND "
			queryTemp += "phoneNumber='" + phoneNumber + "' AND "
			queryTemp += "searchDate='" + date + "')"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchone()
			if str(data[0]) == "1":
				return "TRUE"
			elif str(data[0]) == "0":
				return "FALSE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def insertUserInfo(self, name, socialNumber, companyName, phoneNumber, date):
		try:
			queryTemp = "INSERT INTO userInfo (name, socialNumber, companyName, phoneNumber, searchDate) "
			queryTemp += "VALUES('" + name + "', "
			queryTemp += "'" + socialNumber + "', "
			queryTemp += "'" + companyName + "', "
			queryTemp += "'" + phoneNumber + "', "
			queryTemp += "'" + date + "')"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			return "TRUE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def selectUserInfo(self, name, socialNumber):
		try:
			queryTemp = "SELECT searchDate,companyName,phoneNumber FROM userInfo WHERE "
			queryTemp += "name='" + name + "' AND "
			queryTemp += "socialNumber='" + socialNumber + "' "
			queryTemp += "ORDER BY searchDate"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchall()
			dataList = []
			for row in data:
				dataList.append('!'.join(map(str, row)))
			return '/'.join(dataList)
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def databaseClose(self):
		self.cursor.close()
		self.conn.close()
