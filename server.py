
import socket, threading

debug = True

_connector = None
_running = True

_host = '127.0.0.1'
_port = 12345
_maxClient = 999
_recvBuffer = 2000

def printd (aString):
    if debug:
        print(aString)

class talkToClient (threading.Thread):
    def __init__(self, clientSock, addr):
        self.clientSock = clientSock
        self.addr = addr
        threading.Thread.__init__(self)
    def run (self):
        while True:
            recvData = self.clientSock.recv (_recvBuffer)
            if not recvData:
                self.clientSock.send ('bye')
                break
            printd('Client ' + str (self.addr) + ' say "' + str (recvData.decode()) + '"')
            self.clientSock.send (recvData)
            if recvData == "exit":
                break
        self.clientSock.close ()

_connector = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
_connector.bind ((str(_host), int(_port)))
_connector.listen (int(_maxClient))

while _running:
    printd ('Running on ' + _host + ':' + str (_port) + '.')
    channel, details = _connector.accept ()
    printd ('Conect on : ' + str (details))
    talkToClient (channel, details).start ()

_connector.close ()