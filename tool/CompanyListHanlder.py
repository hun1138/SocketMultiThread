#-*- coding: utf-8 -*-
import sys

import DatabaseHandler

databaseHandler = DatabaseHandler.DatabaseHandler()

while True:
	"""
	print "companyName : ",
	companyName = sys.stdin.readline().strip('\n').strip()
	if companyName == 'exit':
		databaseHandler.databaseClose()
		break;

	print "companyInfo : ",
	companyInfo = sys.stdin.readline().strip('\n').strip()

	query = "INSERT INTO companyInfo(name, info) VALUES('" + companyName + "', '" + companyInfo + "')"
	print query
	"""
	for i in range(3, 16):
		query = "INSERT INTO companyInfo(name, info) VALUES('회사" + str(i) + "', '회사" + str(i) + " 정보')"
		# print query
		databaseHandler.insert(query)
	break;
	# databaseHandler.insert(query)