from socket import *
import threading


class clientRecv(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global running
        while(running):
            modifiedSentence = clientSocket.recv(1024)
            modifiedStr = str(modifiedSentence, encoding='utf-8')
            print("--From server:\n", modifiedStr)

class clientSend(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        global running, threadLock
        while (running):
            sentence = input("Input message:\n")
            sentenceBytes = bytes(sentence, encoding='utf-8')
            clientSocket.send(sentenceBytes)
            if (sentence == ""):
                clientSocket.close()
                threadLock.acquire()
                running = False
                threadLock.release()
                exit(0)


serverName = '10.53.25.16'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

threadLock = threading.Lock()
sendThread = clientSend(1, "send")
recvThread = clientRecv(2, "recv")
running = True
sendThread.start()
recvThread.start()
sendThread.join()
recvThread.join()