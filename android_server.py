import socket
import time

import SocketMultiThread
import DatabaseHandler

# HOST = "192.168.43.149"

HOST = "192.168.0.7"

# HOST = "203.253.21.114"
# HOST = "43.230.2.26"
# HOST = "127.0.0.1"
# HOST = "58.76.178.73"
# HOST = socket.gethostbyname(socket.gethostname())
# HOST = socket.gethostbyname(socket.getfqdn())
PORT = 9999
#ADDR = (HOST, PORT)
BUFF_SIZE = 1024

print HOST
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverSocket.bind((HOST, PORT))
serverSocket.listen(5)


while True:
	try:
		conn, addr = serverSocket.accept()
		print "connection from [%s]" % str(addr)
		databaseHandler = DatabaseHandler.DatabaseHandler()
		SocketMultiThread.SocketThreadHandler(conn, databaseHandler).start()
	except Exception as e:
		print e
		conn.close()
		serverSocket.close()
		databaseHandler.databaseClose()
		break
	except KeyboardInterrupt as e:
		print e
		conn.close()
		serverSocket.close()
		databaseHandler.databaseClose()
		break
