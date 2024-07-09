import socket
import threading
import time
import select

FLEET_ADDRES = "192.168.1.9"
FLEET_PORT = 8015
isConnected = False
ID ='1'

bufferedMessage = ''
#REQUESTVERSION = '0100E903E903010000'
REQUESTVERSION = '00E903E903010000'
HEX_REQUESTVERSION =b'\x01'

RESPONSEHEADER = 'C800E803E90302090000'
ERRORTIMEOUT = 'ERROR TIMEOUT'

class serverSocket:

    connected = False
    def __init__(self, sock=None):
        print("Iniciando Classe do socket")
        global MSGLEN
        MSGLEN = 50
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.settimeout(2)

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
    
    def load_defaults(self):

        RESPONSEHEADER = RESPONSEHEADER
        return

    def is_socket_open(self):
        try:
            # Usa select para verificar a prontidão do socket
            read_ready, _, error_ready = select.select([self.sock], [], [self.sock], 0)
            if read_ready or error_ready:
                return False
            return True
        except socket.error:
            return False

    def sendmessage(self, msg):
        totalsent = 0
        try:
        # Tenta enviar dados
            self.sock.send(msg)
            return True
        except BlockingIOError:
        # Nenhum dado está disponível
            return True
        except socket.error:
        # Outro erro de socket ocorreu
            return False
        
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                #raise RuntimeError("socket connection broken")
                return False
            totalsent = totalsent + sent
        return True

    def recmessage(self):
        chunks = []
        bytes_recd = 0
        try:
            while bytes_recd < MSGLEN:
                chunk = self.sock.recv(41)
                if chunk == b'':
                    print("Error runtime")
                    raise RuntimeError("socket connection broken")
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
                return b''.join(chunks)
        except:
            print("Erro de Conexão")
            self.connected = False
            return ERRORTIMEOUT

    def is_sublist(self,sublist, main_list):
      
        return all(elem in main_list for elem in sublist)

    def ping(self):
        print("Tentando pingar")
        try:
            if self.sendmessage(bytes.fromhex(REQUESTVERSION)):
                if (self.is_sublist(bytes.fromhex(RESPONSEHEADER+'01'),self.recmessage())):
               
                
                    self.connected = True
                    return True
                return False
            else:
                print("Desconectado")
                self.connected = False
                return False
        except:
            return False
    
    def send_lgv_cmd(self):
        print("Tentando pingar")
        try:
            if self.sendmessage(bytes.fromhex(REQUESTVERSION)):
                if (self.is_sublist(bytes.fromhex(RESPONSEHEADER+'01'),self.recmessage())):
               
                
                    self.connected = True
                    return True
                return False
            else:
                print("Desconectado")
                self.connected = False
                return False
        except:
            print("uma cagada qualquer")
            return False

    def sendhex(self,msg):
        print("Tentando Enviar")
        if self.perfconnect() == True :
            print("Conectado")
            hex_number = 20
            hex_bytes = hex_number.to_bytes(2, byteorder='big')
            print(hex_bytes)
            #self.sock.sendall(hex_bytes)
            if self.sendmessage(hex_number.to_bytes(2, byteorder='big')):
                print("Enviou")
                self.connected = True
                return True
            else:
                print("Desconectado")
                self.connected = False
                return False
        else:
            print("Falhou no envio, sem conex.")
            self.connected = False
            return False

    def perfconnect(self):
        return (self.connect(FLEET_ADDRES, FLEET_PORT))


#Wait for new connections



def run():
    global con
    con = serverSocket()
    print(bytes.fromhex('01AF23'))
    #con.connect(FLEET_ADDRES, FLEET_PORT)
    #ping()
    if con.perfconnect() == True:
        con.ping()
        if con.is_sublist(bytes.fromhex(RESPONSEHEADER+'01'),con.recmessage()):
            print("Contém")
        #print("enviando teste")

        #con.sendmessage(bytes.fromhex(REQUESTVERSION))
        #chunk = con.sock.recv(4132)
        #print(chunk)
        
        #print(con.recmessage().decode("utf-8"))

def int_to_two_bytes(number):
    return number.to_bytes(2, byteorder='little')


print(type(REQUESTVERSION))
print(bytes.fromhex(REQUESTVERSION+'01'))
HEX_REQUESTVERSION =bytes.fromhex(REQUESTVERSION)
teste = int_to_two_bytes(int('22')) +( (HEX_REQUESTVERSION ))
print(teste)
#teste = RESPONSEHEADER +'01'
#print(bytes.fromhex(RESPONSEHEADER))
#print(teste)
#REQUESTVERSION = '0100E903E903010000'
#|0x01 0x00 | 0xE9 0x03 | 0x00 0x00  | 0x00    |0x00 0x00
#c8 00 e8 03 e9 03 02\t\x00\x00\x01\x00e\x00\xe8\x03\x00\x00
#C8 00 E8 03 E9 03 02 09 00 00 10 00 00 00 E8 03 00 00
