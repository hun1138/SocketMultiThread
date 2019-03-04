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
		companyData = strTemp.split('/')
		name = companyData[0]
		password = companyData[1]
		strResult = self.databaseHandler.checkLogin(name, password)

		if strResult == "TRUE":

			if name == "admin":
				strResult = "ADMIN"
			else:
				strResult = self.databaseHandler.getCompanyLimitDate(name)
				limitDate = datetime.datetime.strptime(strResult, "%Y-%m-%d")
				# checkDate = userDate + datetime.timedelta(days=30)
				nowDate = datetime.date.today()

				if nowDate.strftime("%Y-%m-%d") > limitDate.strftime("%Y-%m-%d"):
					strResult = "FALSE"
				else:
					strResult = "TRUE/" + self.databaseHandler.getCompanyPhoneNumber(name)

		return strResult

	def addCompanyHandler(self, strTemp):
		companyData = strTemp.split('/')
		name = companyData[0]
		password = companyData[1]
		phoneNumber = companyData[2]

		strResult = self.databaseHandler.checkCompanyNameExist(name)

		if strResult == "FALSE":
			strResult = self.databaseHandler.insertCompany(name, password, phoneNumber)

		strResult = self.databaseHandler.getCompanyLimitDate(name)
		limitDate = datetime.datetime.strptime(strResult, "%Y-%m-%d")
		updateLimitDate = limitDate + datetime.timedelta(days=30)

		strResult = self.databaseHandler.updateCompanyLimitDate(name, updateLimitDate.strftime("%Y-%m-%d"))

		return strResult

	def addInfoHandler(self, strTemp):
		userInfoData = strTemp.split('/')
		name = businessData[0]
		socialNumber = businessData[1]
		companyName = businessData[2]
		phoneNumber = businessData[3]
		date = businessData[4]

		strResult = self.databaseHandler.checkUserInfoExist(name, socialNumber, companyName, phoneNumber, date)

		if strResult == "FALSE":
			strResult = self.databaseHandler.insertUserInfo(name, socialNumber, companyName, phoneNumber, date)

		return strResult


	def searchHandler(self, strTemp):
		userInfoData = strTemp.split('/')
		name = businessData[0]
		socialNumber = businessData[1]
		companyName = businessData[2]
		phoneNumber = businessData[3]
		date = businessData[4]

		strResult = self.databaseHandler.checkUserInfoExist(name, socialNumber, companyName, phoneNumber, date)

		if strResult == "FALSE":
			strResult = self.databaseHandler.insertUserInfo(name, socialNumber, companyName, phoneNumber, date)

		strResult = self.databaseHandler.selectUserInfo(name, socialNumber, companyName, phoneNumber, date)

		return strResult

	def run(self):
		data = self.socket.recv(BUFF_SIZE).strip('\n').strip()
		localtime = time.asctime(time.localtime(time.time()))

		checkData = data.split('#')
		print "[%s] get data : %s" % (localtime, data)

		if checkData[0] == "LOGIN":
			self.socket.send(self.loginHandler(checkData[1]))
		elif checkData[0] == "ADD_COMPANY":
			self.socket.send(self.addCompanyHandler(checkData[1]))
		elif checkData[0] == "ADD_INFO":
			self.socket.send(self.addInfoHandler(checkData[1]))
		elif checkData[0] == "SEARCH":
			self.socket.send(self.searchHandler(checkData[1]))

		print ""

		self.databaseHandler.databaseClose()
		self.socket.close()
