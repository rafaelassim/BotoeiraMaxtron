import socket
import threading
import time

FLEET_ADDRES = "192.168.1.13"
FLEET_PORT = 8015
isConnected = False


bufferedMessage = ''
REQUESTVERSION = '0100E903E903010000'

ERRORTIMEOUT = 'ERROR TIMEOUT'

class serverSocket:

    connected = False
    def __init__(self, sock=None):
        print("Iniciando Classe do socket")
        global MSGLEN
        MSGLEN = 5
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.settimeout(1)

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            self.connected = True
            print("Socket Aceitou a Conexão")
            return True
        except:
            print("Erro de socket connect")
            self.connected = False
            return False
   
    def disconnect(self):
        self.sock.close()

    def sendmessage(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
                return False
            totalsent = totalsent + sent
        return True

    def recmessage(self):
        chunks = []
        bytes_recd = 0
        try:
            while bytes_recd < MSGLEN:
                chunk = self.sock.recv((2048))
                if chunk == b'':
                    raise RuntimeError("socket connection broken")
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
                return b''.join(chunks)
        except:
            print("Erro de Conexão")
            self.connected = False
            return ERRORTIMEOUT

    def ping(self):
        print("Tentando pingar")
        if self.perfconnect() == True :
            if self.sendmessage(bytes.fromhex(REQUESTVERSION)):
                print("Conectado")
                self.connected = True
                return True
            else:
                print("Desconectado")
                self.connected = False
                return False
        else:
            print("Falhou no Ping, sem conex.")
            self.connected = False
            return False

    def perfconnect(self):
        return (self.connect(FLEET_ADDRES, FLEET_PORT))


#Wait for new connections




def run():
    global con
    con = serverSocket()
    print(bytes.fromhex('01AF23'))
    con.connect(FLEET_ADDRES, FLEET_PORT)
    #ping()
    if con.connected == True:
        con.ping()
        time.sleep(5)

        con.sendmessage(bytes.fromhex(REQUESTVERSION))
        print(con.recmessage())
  
