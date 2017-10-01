import threading
import socket
import time

import DatabaseHandler

import datetime

BUFF_SIZE = 1024
"""
INSERT
UPDATE
DELETE
SELECT
"""

ADD_NUM = 50
class SocketThreadHandler(threading.Thread):
	def __init__(self, socket, databaseHandler):
		threading.Thread.__init__(self)
		self.socket = socket
		self.databaseHandler = databaseHandler

	def loginHandler(self, strTemp):
		businessData = strTemp.split('/')
		strResult = self.databaseHandler.checkLogin(businessData)

		if strResult == "TRUE":
			strResult = self.databaseHandler.getBusinessDate(businessData[0])

			if strResult != '0':
				'''
				userDate = datetime.datetime.strptime(strResult, "%Y-%m-%d")
				checkDate = userDate + datetime.timedelta(days=30)
				nowDate = datetime.date.today()

				if nowDate.strftime("%Y-%m-%d") > checkDate.strftime("%Y-%m-%d"):
					strResult = "FALSE"
				else:
					strResult = "TRUE/" + checkDate.strftime("%Y-%m-%d")# strResult
				'''
				businessSearchLimit = self.databaseHandler.getBusinessSearchLimit(businessData[0])
				strResult = "TRUE/" + str(businessSearchLimit)
			elif strResult == '0':
				strResult = "ADMIN"

		return strResult

	def adminInsertHandler(self, strTemp):
		businessData = strTemp.split('/')
		strResult = self.databaseHandler.checkBusinessIDExist(businessData[0])

		if strResult == "FALSE":
			strResult = self.databaseHandler.insertBusiness(businessData, str(ADD_NUM))
			strResult = self.databaseHandler.getBusinessInfo(businessData)
		elif strResult == "TRUE":
			# bDate = self.databaseHandler.getBusinessDate(businessData)
			# strResult = self.databaseHandler.updateBusinessDate(businessData, bDate)
			searchLimitTemp = self.databaseHandler.getBusinessSearchLimit(businessData[0])
			strResult = self.databaseHandler.updateBusinessSearchLimit(businessData[0], str(searchLimitTemp + ADD_NUM))

			strResult = "FALSE"

		return strResult

	def searchHandler(self, strTemp):
		userData = strTemp.split('/')

		searchLimitTemp = self.databaseHandler.getBusinessSearchLimit(userData[3])

		if searchLimitTemp > 0:
			self.databaseHandler.updateBusinessSearchLimit(userData[3], str(searchLimitTemp - 1))

			strResult = self.databaseHandler.checkUserExist(userData)

			if strResult == "FALSE":
				self.databaseHandler.insertUser(userData)

			dataTemp = self.databaseHandler.selectUser(userData)
			self.databaseHandler.updateUser(dataTemp)
			dataTemp = self.databaseHandler.selectUser(userData)

			strResult = self.databaseHandler.checkUserInfoExist(str(dataTemp[0]), userData[3])

			if strResult == "FALSE":
				self.databaseHandler.insertUserInfo(str(dataTemp[0]), userData[3])

			userInfoDataTemp = self.databaseHandler.selectBusinessUserInfo(str(dataTemp[0]), userData[3])
			self.databaseHandler.updateUserInfo(userInfoDataTemp)
			strResult = self.databaseHandler.selectUserInfo(str(dataTemp[0]))

		elif searchLimitTemp <= 0:
			strResult = "FALSE"

		return strResult

	def run(self):
		data = self.socket.recv(BUFF_SIZE).strip('\n').strip()
		localtime = time.asctime(time.localtime(time.time()))

		checkData = data.split('#')
		print "[%s] get data : %s" % (localtime, data)
		
		if checkData[0] == "LOGIN":
			self.socket.send(self.loginHandler(checkData[1]))
		elif checkData[0] == "ADMIN_INSERT":
			self.socket.send(self.adminInsertHandler(checkData[1]))
		elif checkData[0] == "SEARCH":
			self.socket.send(self.searchHandler(checkData[1]))
		elif checkData[0] == "COUNT":
			self.socket.send(str(self.databaseHandler.getBusinessSearchLimit(checkData[1])))

		print ""

		self.databaseHandler.databaseClose()
		self.socket.close()
