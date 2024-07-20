import socket
import threading
import time
import select


isConnected = False

bufferedMessage = ''
RESPONSEHEADER = 'C800E803' 


REQUESTVERSIONID = '0100'
REQUESTVERSION = '0000000000'
HEX_REQUESTVERSION =b'\x01'
HEX_PINGRESPONSE =b'\x01'
HEX_SENDRESPONSE =b'\0x1'
REQUESTORDERID = '1000'


ERRORTIMEOUT = 'ERROR TIMEOUT'

class serverSocket: 
#connected = False
    ID = 0
    FLEET_ADDRES = "192.168.1.10"
    FLEET_PORT = 8015
    def inicializar(self, sock=None):
        print("Iniciando Classe do socket")
        global MSGLEN
        MSGLEN = 50
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    
    def duplicate_ff(self,data):
        result = bytearray()
        for byte in data:
            result.append(byte)
            if byte == 0xff:
                result.append(0xff)
        return result

    def load_defaults(self,ID):
        global HEX_REQUESTVERSION,  REQUESTVERSION, REQUESTVERSIONID, HEX_PINGRESPONSE, RESPONSEHEADER,HEX_SENDRESPONSE
        HEX_REQUESTVERSION = bytes.fromhex(REQUESTVERSIONID) + int_to_two_bytes(ID) + bytes.fromhex(REQUESTVERSION) 
        self.ID = ID
      
        HEX_PINGRESPONSE =  bytes.fromhex(RESPONSEHEADER)+ int_to_two_bytes(ID) + bytes.fromhex('0209000001006500E803000065')
        HEX_SENDRESPONSE =  bytes.fromhex(RESPONSEHEADER)+ int_to_two_bytes(ID) + bytes.fromhex('0209000010000000E8030000')
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
            #Limpando o Buffer
            self.recmessage()
        except:
            print("Não tinha nada no buffer")
        try:
        # Tenta enviar dados
            self.sock.send(msg)
            print("enviou mensagem ")
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
                chunk = self.sock.recv(100000)
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
        print("Comparando", sublist,main_list)
        return all(elem in main_list for elem in sublist)

    def ping(self):
        global HEX_REQUESTVERSION
        print("Tentando pingar")
        print(HEX_REQUESTVERSION)
        loop_var =1
        try:
            if self.sendmessage(HEX_REQUESTVERSION):
                try:
                    while(loop_var <= 2):
                        if (self.is_sublist(HEX_PINGRESPONSE,self.recmessage())):
                    
                            print("recebeu corretamente o ping")
                            self.connected = True
                            return True
                        else:
                            print("Falhou na Checagem")
                        print("Tentando novamente esperar a mensagem")
                        loop_var = loop_var+1
                        time.sleep(0.5)
                    return False
                except:
                    print("Falhou na recepção")
                    self.connected = False
                    return False
            else:
                print("Desconectado")
                self.connected = False
                return False
            print("Falhou na recepção e não acusou falha")
            self.connected = False
            return False
        except:
            print("Falhou no envio")
            self.connected = False
            return False
       
    def configure(self, IP, PORT):
        self.FLEET_ADDRES = IP
        self.FLEET_PORT = PORT
        return

    def send_lgv_cmd(self,maq,prod):
        global REQUESTORDERID,HEX_SENDRESPONSE
        HEX_REQUESMISSION = bytes.fromhex(REQUESTORDERID) + int_to_two_bytes(self.ID) + bytes.fromhex('0000001600FF') +int_to_two_bytes(maq[1])+int_to_two_bytes(prod[1])
        HEX_REQUESMISSION = HEX_REQUESMISSION + int_to_two_bytes(int(maq[0]))+int_to_two_bytes(int(prod[0])) +bytes.fromhex('010001000000000000000000')
        print(HEX_REQUESMISSION)
        print("Tentando enviar lgv")
        HEX_REQUESMISSION = self.duplicate_ff(HEX_REQUESMISSION)
        print(HEX_REQUESMISSION)
        try:
            if self.sendmessage((HEX_REQUESMISSION)):
                print("comando enviado")
                if self.is_sublist(HEX_SENDRESPONSE,self.recmessage()):
                    print("Envio do LGV processado corretamente")                
                    self.connected = True
                    return True
                else:
                    print("Não recebeu confirmação")
                return False
            else:
                print("Desconectado")
                self.connected = False
                return False
        except:
            print("Comando errado")
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
        return (self.connect(self.FLEET_ADDRES, self.FLEET_PORT))


#Wait for new connections



def run():
    global con
    con = serverSocket()
    print(bytes.fromhex('01AF23'))
    #con.connect(FLEET_ADDRES, FLEET_PORT)
    #ping()
    if con.perfconnect() == True:
        con.ping()
        if con.is_sublist(HEX_PINGRESPONSE,con.recmessage()):
            print("Contém")
        #print("enviando teste")

        #con.sendmessage(bytes.fromhex(REQUESTVERSION))
        #chunk = con.sock.recv(4132)
        #print(chunk)
        
        #print(con.recmessage().decode("utf-8"))

def int_to_two_bytes(number):
    return number.to_bytes(2, byteorder='little')

#con = serverSocket()
#con.perfconnect()
#con.load_defaults(int(1001))
#con.send_lgv_cmd(('415', 1),('415', 1))
#p#rint(type(REQUESTVERSION))
#p#rint(bytes.fromhex(REQUESTVERSION+'01'))
#HEX_REQUESTVERSION =bytes.fromhex(REQUESTVERSION)
#teste = int_to_two_bytes(int('22')) +( (HEX_REQUESTVERSION ))
#data = bytes([0xff, 0x03])
#test_data = [
#    bytes([0x00, 0xfe, 0x03, 0x00]),
#    bytes([0xff, 0x03]),
#    bytes([0x00, 0x03]),
#    bytes([0x01, 0x03]),
#]
#int.from_bytes(data, "big")
#byte_val = b'\xff\x03'
#01 00 E9 03 00 00 00 00 00
#01 00 02 00 00 00 00 00 00
#print(HEX_REQUESTVERSION)
#con.sock.sendall(HEX_REQUESTVERSION)
#con.ping()
#con.sock.sendall(b'\x03\xff')
#print(f'Bytes {data.hex()} enviados')
        
 
# converting to int
# byteorder is big where MSB is at start
#int_val = int.from_bytes(byte_val, "big")
 
# printing int equivalent
#sprint(int_val)
#teste = RESPONSEHEADER +'01'
#print(bytes.fromhex(RESPONSEHEADER))
#print(teste)
#REQUESTVERSION = '0100E903E903010000'
#|0x01 0x00 | 0xE9 0x03 | 0x00 0x00  | 0x00    |0x00 0x00
#c8 00 e8 03 e9 03 02\t\x00\x00\x01\x00e\x00\xe8\x03\x00\x00
#C8 00 E8 03 E9 03 02 09 00 00 10 00 00 00 E8 03 00 00
