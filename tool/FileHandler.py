import os
import struct

BUFF_SIZE = 1024

class FileHandler:
	def __init__(self, socket, dirName):
		self.socket = socket
		self.folder = os.getcwd() + '/' + dirName

	def saveFile(self, fileName):
		try:
			fileOpen = open(self.folder + '/' + fileName, "wb")
			while True:
				byteString = self.socket.recv(BUFF_SIZE)
				if not byteString:
					break
				fileOpen.write(byteString)
			fileOpen.close()
			"""
			buf = ''
			print "buf : %s" % (4 - len(buf))
			while len(buf) < 4:
				print buf
				buf += self.socket.recv(4 - len(buf))
			print "buf : %s" % buf
			size = struct.unpack('!i', buf)
			print "receiving %s bytes" % size

			with open(self.folder + '/' + fileName, 'wb') as img:
			    while True:
			        data = self.socket.recv(1024)
			        if not data:
			            break
			        img.write(data)
			"""
			print 'File received'
		except Exception as e:
			print e

	def getFile(self, fileName):
		try:
			fileOpen = open(self.folder + '/' + fileName, "rb")
			byteString = ""
			while True:
				byteString += fileOpen.readline(BUFF_SIZE)
				if not byteString:
					break
			socket.send(byteString)
			fileOpen.close()
		except Exception as e:
			print e

	def getDirectory(self):
		return self.folder