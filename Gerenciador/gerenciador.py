from random import randbytes
import time

# Forma da Mensagem: start_byte hearte_beat inq_request control__bytes product machine_selected crc end_byte
# 0x02 0x0X 
default_machine = [0x00]
default_product = [0x00, 0x00, 0x00, 0x00, 0x00]

start_byte = [0x02]
heart_beat = [0x00]
inq_request = []
control_bytes = [0x00, 0x00, 0x00, 0x00, 0x00]  # bytes de controle numero aleatório gerado, quando a mensagem recebida conter o mesmo que este a ultima requisação pode ser apagada
n_control_bytes = 5 # numero total de bytes de controle

product = [] # dado do scanner manual
n_product = 20 # número de bytes vindos do scanner manual 
machine_selected =[0x00] #número da máquina selecionada
crc = []    # crc é um xor da dos bytes a serem enviados
end_byte = [0x03]
strikes = 0
max_strikes = 10
passed_heart_beat =[0]

def process_message(message):
    global strikes
    global product
    global machine_selected
    global passed_heart_beat
    control_bytes_rec =[0x00, 0x00, 0x00, 0x00, 0x00] 
    control_bytes_rec[0] = message[2]
    control_bytes_rec[1] = message[3]
    control_bytes_rec[2] = message[4]
    control_bytes_rec[3] = message[5]
    control_bytes_rec[4] = message[6]
    
    
    if strikes >= max_strikes:
        print('Strikes Excedeu o máximo')

    if confirm_message_integrity(message)==True:
        print('CRC Recebimento confere')
    else: 
        strikes=+1
        return False

    if passed_heart_beat[0]==message[1]:
        strikes=+1
       
        return False
    else:
        passed_heart_beat[0]=message[1]
        print('Heart Beat Passou')
        strikes=0
   
    if control_bytes_rec==control_bytes:
        machine_selected=default_machine
        product=default_product
        print("Clean Product?")
    print("Control Bytes rec",control_bytes_rec)
    print("Control Bytes",control_bytes)
    return True
      
    


def generate_heart_bit():
    global heart_beat
    if heart_beat[0]==1:
        heart_beat[0]=0
    else:
        heart_beat[0]=1

def string_to_list_bytes(string):
    bytes_list = list(string.encode('ascii'))
    return bytes_list

def generate_material():
    maii =0

    
def generate_machine(machine_input):
    
    machine=[]
    machine = string_to_list_bytes(machine_input)
    machine_selected[0]=machine[0]
   


def create_random():
    global control_bytes
    rand = randbytes(n_control_bytes)
    n = len(rand)
    for i in range (n):
        control_bytes[i] = rand[i]
    #control_bytes = [0x00,0x01,0x02,0x03,0x04]
    
    
#calcula o CRC da mensagem
def crc_calculation (message):
    n = len(message)
    xor = 0
    for i in range (n):
        xor = xor ^ message[i]
        t = message[i]
    return [xor]

#confirma integridade da mensagem
def confirm_message_integrity(message):
    passed = False
    if message[len(message)-1] != end_byte[0] :
        print("End_byte não confere")
        return False
    n = len(message) - 2
    xor = 0
    for i in range (n):
        xor = xor ^ message[i]
        t = message[i]
    if xor == message[len(message) - 2] :
        print("CRC Confere")
        passed = True
    return passed

#cria a mensagem no formato padrão esperado pelo servidor
def create_message():


    if machine_selected[0]==default_machine[0] :
        create_random()
    
    generate_heart_bit()
    message = []
    message = start_byte + heart_beat + inq_request+ control_bytes + product + machine_selected
    #message = start_byte + heart_beat + inq_request+ control_bytes + machine_selected
    print(message)
    print("machine",machine_selected)
    print("data scanner",product)
    #print ("Xor ", crc_calculation(message))
    message = message + crc_calculation(message)+ end_byte
    #print ("Xor ", crc_calculation(message))
    confirm_message_integrity(message)
    return message

def blink_heart_beat():
    
    while True:
        heart_beat[0] = 0x01
        print(hex(heart_beat[0]))
        time.sleep(1)
        heart_beat[0] = 0x00
        print(hex(heart_beat[0]))
        time.sleep(1)

class message_from_listener ():

    isconnected = False

    heart_bit = False
    had_message = False
    message =[]

class message_to_listener ():
    send_message = False
    heart_bit = False
    barcode = ''
    date_from_listener = ''
    message = []