import os
import sys
import FileHandler

folder = os.getcwd()
print "folder: %s" % folder
for filename in os.listdir(folder):
	print filename
	fullname = os.path.join(folder, filename)
	#print fullname


print "\n****************************"
print os.getcwd()

print os.path.realpath(__file__)
print os.path.dirname(os.path.realpath(__file__))

filehandler = FileHandler.FileHandler("img")
stringByte = filehandler.getFile("sample_04.jpg")
print sys.getsizeof(stringByte)
# filehandler.saveFile("sample_05.jpg", stringByte)
