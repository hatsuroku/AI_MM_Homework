from socket import *

serverName = '192.168.1.108'
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
message = bytes(input('Input lowercase sentence:'), encoding='utf-8')
clientSocket.sendto(message, (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
modifiedString = str(modifiedMessage, encoding='utf-8')
print(modifiedString)
clientSocket.close()