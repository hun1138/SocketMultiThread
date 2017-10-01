import socket
import sys

# HOST = "43.230.2.142"
HOST = "127.0.0.1"
PORT = 9999
# BUFF_SIZE = 1024
# ADDR = (HOST, PORT)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect((HOST, PORT))

message = sys.stdin.readline()
clientSocket.send(message)

clientSocket.close()