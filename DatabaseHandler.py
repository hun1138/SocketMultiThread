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
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS user(
			ID INT PRIMARY KEY AUTO_INCREMENT,
			userName CHAR(10) NOT NULL,
			socialSecurityNumber CHAR(20) NOT NULL,
			phoneNumber CHAR(16) NOT NULL,
			searchTotalCount INT NOT NULL)
			ENGINE=INNODB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_general_ci;
			""")
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS userInfo(
			ID INT PRIMARY KEY AUTO_INCREMENT,
			userID INT NOT NULL,
			businessIdentification CHAR(20) NOT NULL,
			lastSearchDate CHAR(20),
			searchCount INT NOT NULL,
			FOREIGN KEY (userID) REFERENCES user(ID) ON DELETE CASCADE)
			ENGINE=INNODB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_general_ci;
			""")
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS business(
			ID INT PRIMARY KEY AUTO_INCREMENT,
			identification CHAR(20) NOT NULL,
			password CHAR(20) NOT NULL,
			searchLimit INT NOT NULL,
			signInDate CHAR(20))
			ENGINE=INNODB DEFAULT CHARACTER SET = utf8 COLLATE = utf8_general_ci;
			""")
		'''
		
		self.conn.commit()
# password('password')
	# LOGIN
	def checkLogin(self, businessData):
		try:
			queryTemp = "SELECT EXISTS(SELECT * FROM business WHERE "
			queryTemp += "identification='" + businessData[0] + "' AND "
			queryTemp += "password='" + businessData[1] + "')"

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

	def getBusinessDate(self, businessIdentification):
		try:
			queryTemp = "SELECT signInDate FROM business WHERE "
			queryTemp += "identification='" + businessIdentification + "'"
			# queryTemp += " AND password='" + businessData[1] + "'"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchone()
			return data[0]
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def getBusinessSearchLimit(self, businessIdentification):
		try:
			queryTemp = "SELECT searchLimit FROM business WHERE "
			queryTemp += "identification='" + businessIdentification + "'"
			# queryTemp += " AND password='" + businessData[1] + "'"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchone()
			return data[0]
		except Exception as e:
			print e
			return ERROR_MESSAGE

	# ADMIN_INSERT
	def checkBusinessIDExist(self, businessData):
		try:
			queryTemp = "SELECT EXISTS(SELECT * FROM business WHERE "
			queryTemp += "identification='" + businessData + "')"

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

	def insertBusiness(self, businessData, addNum):
		try:
			nowDate = datetime.date.today()
			queryTemp = "INSERT INTO business (identification, password, signInDate, searchLimit) "
			queryTemp += "VALUES('" + businessData[0] + "', " 
			queryTemp +=	"'" + businessData[1] + "', "
			queryTemp += "'" + nowDate.strftime("%Y-%m-%d") + "', " + addNum + ")"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchone()
			return "TRUE"
		except Exception as e:
			print e
			return ERROR_MESSAGE	

	def getBusinessInfo(self, businessData):
		try:
			queryTemp = "SELECT identification,password FROM business WHERE "
			queryTemp += "identification='" + businessData[0] + "' AND "
			queryTemp += "password='" + businessData[1] + "'"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchone()
			return str(data[0]) + '/' + str(data[1])
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def updateBusinessSearchLimit(self, businessIdentification, searchLimitTemp):
		try:
			queryTemp = "UPDATE business SET searchLimit=" + searchLimitTemp + " "
			queryTemp += "WHERE identification='" + businessIdentification + "'"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			return "TRUE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	
	'''
	def updateBusinessDate(self, businessData, bDate):
		try:
			userDate = datetime.datetime.strptime(bDate, "%Y-%m-%d")
			inDate = userDate + datetime.timedelta(days=30)

			queryTemp = "UPDATE business SET signInDate='" + inDate.strftime("%Y-%m-%d") + "' "
			queryTemp += "WHERE identification='" + businessData[0] + "'"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			return "TRUE"
		except Exception as e:
			print e
			return ERROR_MESSAGE
	'''

	# SEARCH
	def checkUserExist(self, userData):
		try:
			queryTemp = "SELECT EXISTS(SELECT * FROM user WHERE "
			queryTemp += "userName='" + userData[0] + "' AND "
			queryTemp += "socialSecurityNumber='" + userData[1] + "')"
                        # queryTemp += "' AND phoneNumber='" + userData[2] + "')"

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

	def insertUser(self, userData):
		try:
			queryTemp = "INSERT INTO user (userName, socialSecurityNumber, phoneNumber, searchTotalCount) "
			queryTemp += "VALUES('" + userData[0] + "', " 
			queryTemp +=	"'" + userData[1] + "', "
			queryTemp +=	"'" + userData[2] + "', 0)"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			return "TRUE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def selectUser(self, userData):
		try:
			queryTemp = "SELECT ID,searchTotalCount FROM user WHERE "
			queryTemp += "userName='" + userData[0] + "' AND "
			queryTemp += "socialSecurityNumber='" + userData[1] + "'"
			# queryTemp += " AND phoneNumber='" + userData[2] + "'"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchall()
			return data[0]
		except Exception as e:
			print e
			return ERROR_MESSAGE

	# dataTemp[0] = user_ID, dataTemp[1] = user_searchTotalCount
	def updateUser(self, dataTemp):
		try:
			queryTemp = "UPDATE user SET searchTotalCount=" + str(dataTemp[1] + 1) + " "
			queryTemp += "WHERE ID=" + str(dataTemp[0])

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			return "TRUE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def checkUserInfoExist(self, userID, businessIdentification):
		try:
			queryTemp = "SELECT EXISTS(SELECT * FROM userInfo WHERE "
			queryTemp += "userID=" + userID + " AND "
			queryTemp += "businessIdentification='" + businessIdentification + "')"

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

	def insertUserInfo(self, userID, businessIdentification):
		try:
			queryTemp = "INSERT INTO userInfo (userID, businessIdentification, searchCount) "
			queryTemp += "VALUES(" + userID + ", " 
			queryTemp +=	"'" + businessIdentification + "', 0)"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			return "TRUE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def selectBusinessUserInfo(self, userID, businessIdentification):
		try:
			queryTemp = "SELECT ID,searchCount FROM userInfo WHERE "
			queryTemp += "userID=" + userID + " AND "
			queryTemp += "businessIdentification='" + businessIdentification + "'"

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			data = self.cursor.fetchall()
			return data[0]
			
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def selectUserInfo(self, userID):
		try:
			queryTemp = "SELECT businessIdentification,searchCount,lastSearchDate FROM userInfo WHERE "
			queryTemp += "userID=" + userID

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

	def updateUserInfo(self, dataTemp):
		try:
			nowDate = datetime.date.today()
			queryTemp = "UPDATE userInfo SET searchCount=" + str(dataTemp[1] + 1) + ","
			queryTemp += "lastSearchDate='" + nowDate.strftime("%Y-%m-%d") + "' "
			queryTemp += "WHERE ID=" + str(dataTemp[0])

			print queryTemp

			self.cursor.execute(queryTemp)
			self.conn.commit()

			return "TRUE"
		except Exception as e:
			print e
			return ERROR_MESSAGE

	def databaseClose(self):
		self.cursor.close()
		self.conn.close()
