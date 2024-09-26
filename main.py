#import Server.server as server
#import Server.server as server
#import Network.network as network
import USB_Service.usb as usbservice
import Barcode.barcode as barcode
import Gerenciador.gerenciador as gerenciador
import DataReader.datareader as datareader
import threading
import Maxtron.Maxtron_Interface as maxtron
import time as time
import serial



region_tot = 0
region_nome = []

maquinas_tot = 0
maquinas_nome = []

produto_tot = 0
produtos_bitola = []

produtos_bitola_tot =0
produtos_bitola_nomes =[]

barcode_msg = ''
keyboard_msg = ''
#REGIAO ="A"
#MAQUINA ="MAQUINA A"
block_minus_plus = False
increment = False
decrement = False

class MAQUINA:
    #id_machine":5,"Nome":"strech","material_type": "BOBINA,PALLET","action_type":"ABASTECE,RETIRA,ABASTECE_ENTRADA,ABASTECE_SAIDA,RETIRA_ENTRADA,RETIRA_SAIDA","situation": "COMPLETO,INCOMPLETO"
    id_machine = 1
    Nome = "Default"
    #material_type = "BOBINA"
    action_type = "ABASTECE"
    situation = "COMPLETO"

    def info(self):
        return f"id_machine: {self.id_machine}, Nome: {self.Nome}, action_type: {self.action_type} , situation: {self.situation}"
class PRODUTO:
    #id_machine":5,"Nome":"strech","material_type": "BOBINA,PALLET","action_type":"ABASTECE,RETIRA,ABASTECE_ENTRADA,ABASTECE_SAIDA,RETIRA_ENTRADA,RETIRA_SAIDA","situation": "COMPLETO,INCOMPLETO"
    SKU = 123456
    material_type = "BOBINA"
    gauge = "0.8"
    product = "0,8 BE14"
   

    def info(self):
        return f"SKU: {self.SKU}, gauge: {self.gauge} , material_type: {self.material_type}, product: {self.product}"

def read_barcode():
    global barcode_msg
    while True:
        if barcode_msg == '':
            barcode_msg=barcode.read()

        else :
            time.sleep(1)

def read_keyboard():
    global keyboard_msg
    global increment
    global decrement
    global block_minus_plus
    increment=False
    decrement=False
    
    print("Iniciando teclado")
    while True:
        if keyboard_msg == '':
            keyboard_msg=main_menu.read_button_press()
            if not block_minus_plus:
                if keyboard_msg == 'F1':
                    keyboard_msg=''
                    increment = True
                    print("increment")
                if keyboard_msg == 'F2':
                    keyboard_msg=''
                    decrement = True
                    print("decrement")
            time.sleep(0.1)
        else :
            time.sleep(0.250)
           
            keyboard_msg=''

def checkconnection ():
    while True:
        fleetManager.heartbeat()
        time.sleep(3)
    
        
def processo_selecao(pointer, maxsize, array, usebarcode):
    global increment
    global decrement
    global block_minus_plus
    global barcode_msg
    
    main_menu.clear_l2()
    time.sleep(0.250)
    if (len(array[pointer]) > 8):
        main_menu.write_dinamic_line2(array[pointer])
    else:
        main_menu.write_line2(array[pointer])      
    while True:
        if decrement:
            pointer = pointer-1
        if increment:
            pointer = pointer+1
        if  pointer >= maxsize :
            pointer = maxsize -1
        if  pointer < 0:
                pointer = 0
        if decrement or increment :
            increment = False
            decrement = False
            main_menu.clear_l2()
            if (len(array[pointer]) > 8):
                main_menu.write_dinamic_line2(array[pointer])
            else:
                main_menu.write_line2(array[pointer])
        if keyboard_msg=='ENT':
            time.sleep(0.250)
            return array[pointer]

        if keyboard_msg =='CLR':
                time.sleep(0.250)
                break    
        if is_number_ascii(str(keyboard_msg))==True: 
            print("Tecla encontrada")
            block_minus_plus=True
            processo_digitacao_teclado(pointer, maxsize, array)
            block_minus_plus=False
        if barcode_msg !='' and usebarcode:
            return


    

def is_number_ascii(input_str):
    for char in input_str:
        if ( 48 <= ord(char) <= 57) and (input_str!=None)and (input_str!='None') and (len(input_str)==1):  # ASCII values for digits 0 to 9
            print("Encontrou a tecla:",input_str)
            return True
    return False

def processo_digitacao_teclado(pointer, maxsize, array):
    global keyboard_msg
    completed = False
    main_menu.clear_l2()
    display_msg =''
    while not completed:
        if keyboard_msg !='':
            if keyboard_msg=='ENT':
                completed=''
                if display_msg in array:
                    print("Contem o item")
                    return
                else:
                    print("Nao contem o item ",display_msg)
                    main_menu.clear_l2()
                    display_msg =''
                    keyboard_msg=''
                    time.sleep(0.1)
                    keyboard_msg=''
                    time.sleep(0.1)
                    keyboard_msg=''
                    return
            elif keyboard_msg=='CLR':
                main_menu.clear_l2()
                display_msg ='' 
            elif is_number_ascii(str(keyboard_msg))==True:   
                try:
                    display_msg=display_msg+keyboard_msg
                    keyboard_msg=''
                    main_menu.write_line2(display_msg)
                except:
                    keyboard_msg=''
            else :
                keyboard_msg=''
    return

def enviar_command(maquina,produto):
    global keyboard_msg
    main_menu.execute_command('Azul ON')
    main_menu.execute_command('Verde OFF')
    main_menu.execute_command('Vermelho OFF')
    main_menu.clear_display()
    main_menu.write_line1('ENVIANDO ')
    main_menu.write_dinamic_line2('AGUARDE... ')
    keyboard_msg =''
    ret = False
    while (not ret):
        
        for i in range(50):
            
           
            if keyboard_msg=='CLR':
                main_menu.execute_command('Azul OFF')
                main_menu.execute_command('Verde OFF')
                main_menu.execute_command('Vermelho ON')
                main_menu.clear_display()
                main_menu.write_line1('PEDIDO')
                main_menu.write_dinamic_line2('CANCELADO')
                time.sleep(8)
                return
         
            time.sleep(0.100)
        server_response = fleetManager.send_command(maquina,produto)
        ret = server_response.ret
        if (not ret):
            if (len(server_response.message) > 8):
                main_menu.write_dinamic_line2(server_response.message)
            else:
                main_menu.write_line1(server_response.message)
            time.sleep(8)
    if (ret==True):
        main_menu.execute_command('Azul ON')
        main_menu.execute_command('Verde ON')
        main_menu.execute_command('Vermelho ON')
        main_menu.clear_display()
        main_menu.write_line1('PEDIDO')
        #main_menu.write_dinamic_line2('REALIZADO')
        if (len(server_response.message) > 8):
            main_menu.write_dinamic_line2(server_response.message)
        else:
            main_menu.write_line1(server_response.message)
        time.sleep(8)
    return



def pedido_viateclado():
    
    
    time.sleep(0.1)
    keyboard_msg=''
   
  
    maquina = sel_maq()
    if maquina is None:
        print("Faltou a maquina")
        return
    
    produto = sel_prod()
    if produto is None:
        print("Faltou Produto")
        return
    enviar_command(maquina,produto)
    return
    try:
        keyboard_msg=''
        
        if tag_maq['MissionType']!=5:
            if tag_produto["Tag"] != 0:
                enviar_command(tag_maq,tag_produto)
                    
            else:
                main_menu.execute_command('Azul ON')
                main_menu.execute_command('Verde ON')
                main_menu.execute_command('Vermelho OFF')
                main_menu.clear_display()
                main_menu.write_line1('OPS!')
                main_menu.write_dinamic_line2('TENTE NOVAMENTE')
                time.sleep(10)
        else:
            print("Se maq. é para descarte envia sem selecionar produto")
               
            enviar_command(tag_maq,tag_maq)
        
    except:
        print("Retornando ao menu")
    return


def sel_prod():
    global REGIAO
    global barcode_msg
    prod=PRODUTO()
   
    pointer = 0
    produto_lista = datareader.return_product()
    qrcode_list = datareader.return_qrproduct()
    main_menu.write_line1('Sel.Bito')

    bitola_selecionada=processo_selecao(pointer, len(produto_lista.keys()), list(produto_lista.keys()),True)  
    if barcode_msg !='':
        if barcode_msg in qrcode_list:
            qrcode = barcode_msg
            barcode_msg=""
            prod.SKU=qrcode
            print("Produto ",qrcode," encontrado")
            return prod
        else :
            main_menu.write_line1('  OPS!  ')
            main_menu.write_line2('        ')
            print("Produto ",barcode_msg," não encontrado")
            barcode_msg=""
            time.sleep(10)
            return
          
    print("Bitola Selecionada", bitola_selecionada)
    prod.gauge = bitola_selecionada
    
    main_menu.write_line1('Produto ')
    produto_selecionado = processo_selecao(pointer, len(produto_lista[bitola_selecionada].keys()), list(produto_lista[bitola_selecionada].keys()),False) 
    print("Produto Selecionado", produto_selecionado)
    prod.product = produto_selecionado
    
    prod.SKU = produto_lista[prod.gauge][prod.product]["SKU"]
    prod.material_type = produto_lista[prod.gauge][prod.product]["material_type"]
    print(prod.info())
    return prod



def sel_maq():
    global REGIAO
    global barcode_msg

    maq = MAQUINA()
    pointer = 0
    regiao_selecionada = datareader.return_maquinas(REGIAO)
    if barcode_msg =='':
        barcode_msg =""
        main_menu.write_line1('Sel.Maq.')
        maquina_selecionada=processo_selecao(pointer, len(regiao_selecionada), list(regiao_selecionada),False)    
    else:
        maquina_selecionada = barcode_msg
        barcode_msg =""
        if maquina_selecionada in regiao_selecionada:
            print("Pedido via Scanner")
        else:
            main_menu.write_line1('  OPS! ')
            main_menu.write_line2('        ')
            print("Maquina ",maquina_selecionada," não encontrada")
            time.sleep(10)
            return

    print("Maquina selecionada", maquina_selecionada)
    maq.id_machine=regiao_selecionada[maquina_selecionada]["id_machine"]
    maq.Nome=regiao_selecionada[maquina_selecionada]["Nome"]
    pointer = 0
    main_menu.write_line1('Sel.Mat.  ')
    #tipo_material=processo_selecao(pointer, len(regiao_selecionada[maquina_selecionada]["material_type"].split(',')), list(regiao_selecionada[maquina_selecionada]["material_type"].split(',')),False)
    #print("Tipo de Material selecionado", tipo_material)
    #maq.material_type=tipo_material


    pointer = 0
    main_menu.write_line1('Movimenta')
    tipo_acao=processo_selecao(pointer, len(regiao_selecionada[maquina_selecionada]["action_type"].split(',')), list(regiao_selecionada[maquina_selecionada]["action_type"].split(',')),False)
    print("Tipo de Ação selecionado", tipo_acao)
    maq.action_type=tipo_acao

    pointer = 0
    main_menu.write_line1('Situacao')
    tipo_situacao=processo_selecao(pointer, len(regiao_selecionada[maquina_selecionada]["situation"].split(',')), list(regiao_selecionada[maquina_selecionada]["situation"].split(',')),False)
    print("Tipo de Situação selecionado", tipo_situacao)
    maq.situation=tipo_situacao
    print(maq.info())
    return maq

   




def gerenciador_encontrado(main_menu):
    main_menu.execute_command('Azul OFF')
    main_menu.execute_command('Verde ON')
    main_menu.execute_command('Vermelho OFF')
    main_menu.clear_display()
    main_menu.write_line1('TUNKERS ')
    main_menu.write_line2('BOTOEIRA')
    time.sleep(0.1)
    return

def gerenciador_n_encontrado(main_menu):
    main_menu.execute_command('Azul OFF')
    main_menu.execute_command('Verde OFF')
    main_menu.execute_command('Vermelho ON')
    #main_menu.clear_display()
    main_menu.write_line1('BOTOEIRA ')
    main_menu.write_dinamic_line2('Sem Conex.  ')
    time.sleep(0.1)
    return

def gerenciador_proc_message(main_menu):
    main_menu.execute_command('Azul ON')
    main_menu.execute_command('Verde OFF')
    main_menu.execute_command('Vermelho OFF')


if __name__ == '__main__':
      
    global total_connections
    global REGIAO
   

    #print(len(datareader.region_list()))
    region_tot = len(datareader.region_list())
    region_nome = datareader.region_list()

    produto_tot = len(datareader.produto_bitola_list())
    produtos_bitola = datareader.produto_bitola_list()
    main_menu = maxtron.init()

    config=datareader.config()
    #print(config)
    REGIAO=config["REGIAO"]
    
    print("Iniciando")
    t = time.perf_counter()
    fleetManager = gerenciador.serverSocket()


    #gerenciador.serverSocket.configure(config["IP-GERENCIADOR"],config["PORT"],config["ID"])
    fleetManager.configure(config["IP-GERENCIADOR"],config["PORT"],config["ID"])
  

    #network.initnetwork(config)
    
    thread_usb= threading.Thread (target=usbservice.monitor_usb,args=(main_menu,))
    thread_barcode = threading.Thread(target=read_barcode)
    thread_keyboard = threading.Thread(target=read_keyboard)
    thread_checkconnection = threading.Thread(target=checkconnection)

    thread_checkconnection.start()
    thread_barcode.start()
    thread_keyboard.start()
    thread_usb.start()
    while True:
        
        elapsed_time = time.perf_counter() - t
        time.sleep(0.2)
        if(fleetManager.CONNECTED ==True):
            if barcode_msg != '':
                #pedido_viascanner()
                pedido_viateclado()

        if (1==1):
            if keyboard_msg !='':
                if keyboard_msg == 'PUSH':
                    keyboard_msg=''
                    pedido_viateclado()

        if ((time.perf_counter() - t)>(10)):
            t = time.perf_counter()
        #    checkconnection()
            if(fleetManager.CONNECTED ==True):
                print('Conectado')
                gerenciador_encontrado(main_menu)
            else:
                print('Não conectado')
                gerenciador_n_encontrado(main_menu)
                
           
