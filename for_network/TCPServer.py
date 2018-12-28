from socket import *
import threading

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(2)
print("The server is ready to receive.\n")
connectionSocket, addr = serverSocket.accept()

class serverSend (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global running, threadLock
        while (running):
            reply = input("--Reply:\n")
            replyBytes = bytes(reply, encoding='utf-8')
            connectionSocket.send(replyBytes)
            if (reply == ""):
                connectionSocket.close()
                threadLock.acquire()
                running = False
                threadLock.release()
                exit(0)

class serverRecv (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global running
        while (running):
            sentence = connectionSocket.recv(1024)
            sentenceStr = str(sentence, encoding='utf-8')
            print("Received:\n", sentenceStr)


sendThread = serverSend(1, "send")
recvThread = serverRecv(2, "recv")
threadLock = threading.Lock()
running = True
sendThread.start()
recvThread.start()
sendThread.join()
recvThread.join()