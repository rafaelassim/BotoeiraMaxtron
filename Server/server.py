import socket
import threading
import time


#Variables for holding information about connections
connections = []
total_connections = 0
kill_thread = False
default_timeout = 20     #timeout para resetar a o server
default_message_size = 3 #Filtro para o tamanho certo da mensagem
#Client class, new instance created for each connected client
#Each instance has the socket and address that is associated with items
#Along with an assigned ID and a name chosen by the client
class recv(threading.Thread):
    def __init__(self, socket, address, id, name, signal, gerenciador):
        threading.Thread.__init__(self)

        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
        self.gerenciador = gerenciador
        print(gerenciador.message_to_listener.barcode)
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    def run(self):
        global send_message
        global kill_thread
        data=''
        strikes = 0
        while self.signal:
            try:
                data = self.socket.recv(1024)
            
            except socket.timeout:
                # Se ocorrer um timeout, significa que o cliente está inativo
                print("Timeout. Cliente pode estar inativo.")
                kill_thread = True
                self.signal = False
                connections.remove(self)
            except ConnectionResetError:
                print("Error")
                kill_thread = True
                self.signal = False
                connections.remove(self)
            if len(data) > 0:
                #print("ID " + str(self.id) + ": " + str(data.decode("utf-8")))
                #print(len(data))
                self.gerenciador.process_message(data)
                #self.gerenciador.message_to_listener.message= data
                #self.gerenciador.message_to_listener.send_message = True
                data= ""
            else :
                strikes +=1
            
            if strikes > 10:
                kill_thread = True
                self.signal = False
                connections.remove(self)
                time.sleep(20)
    def join(self, timeout=None):
        """ Stop the thread. """
        #self._stopevent.set(  )
        threading.Thread.join(self, timeout)


class send(threading.Thread):
    def __init__(self, socket, address, id, name, signal, gerenciador):
        threading.Thread.__init__(self)
        self.socket = socket
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
        self.gerenciador = gerenciador
    def __str__(self):
        return str(self.id) + " " + str(self.address)
    
    #Attempt to get data from client
    #If unable to, assume client has disconnected and remove him from server data
    #If able to and we get data back, print it in the server and send it back to every
    #client aside from the client that has sent it
    #.decode is used to convert the byte data into a printable string
    def run(self):
        global kill_thread
        while self.signal:
           
            if kill_thread : 
                self.signal = False 
                print("Stoped Waiting signal")

            if self.gerenciador.message_to_listener.send_message :
                try:
                    self.socket.sendall(bytes(self.gerenciador.create_message()))
                    self.gerenciador.message_to_listener.send_message = False
                except:
                    print("Error on send")
                    self.gerenciador.message_to_listener.send_message = False

    def join(self, timeout=None):
        """ Stop the thread. """
        #self._stopevent.set(  )
        threading.Thread.join(self, timeout)    
         
class looping(threading.Thread):
    def __init__(self, socket, address, id, name, signal, gerenciador):
        threading.Thread.__init__(self)
        self.address = address
        self.id = id
        self.name = name
        self.signal = signal
        self.gerenciador = gerenciador

    def run(self):
        global kill_thread
        while self.signal:
            self.gerenciador.message_to_listener.send_message = True
            time.sleep(1)
            if kill_thread : 
                self.signal = False 
                print("Stoped Waiting signal")
            if self.gerenciador.strikes >= self.gerenciador.max_strikes:
                kill_thread=True
                self.gerenciador.strikes = 0
       

#Wait for new connections
def newConnections(socket,gerenciador):
    print ("Initiated Server")
    global kill_thread
    global default_timeout
    while True:
       
        sock, address = socket.accept()
        global total_connections
        total_connections=0
        sock.settimeout(default_timeout)

        connections.append(recv(sock, address, total_connections, "Recv", True, gerenciador))
        connections[len(connections) - 1].start()

        connections.append(send(sock, address, total_connections, "Send", True, gerenciador))
        connections[len(connections) - 1].start()

        connections.append(looping(sock, address, total_connections, "looping", True, gerenciador))
        connections[len(connections) - 1].start()

        print("New connection at ID " + str(connections[len(connections) - 1]))
        total_connections += 1
        while kill_thread == False : 
          
            time.sleep(10)
        total_connections=0
        connections[len(connections) - 1].join()
        connections[len(connections) - 2].join()
        connections[len(connections) - 3].join()
        kill_thread = False
        print("Server Threads Killed")
        


def run(gerenciador):
    #Get host and port
    host = ''#input("Host: ")
    port = 6898#int(input("Port: "))
     #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    #Create new thread to wait for connections
    newConnectionsThread = threading.Thread(target = newConnections, args = (sock,gerenciador,))
    newConnectionsThread.start()

print ("Initiated")
#reserved to initialize variables