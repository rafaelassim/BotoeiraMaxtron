#import Server.server as server
import Server.server as server
import rest.rest_api as rest
import Barcode.barcode as barcode
import Gerenciador.gerenciador as gerenciador
import DataReader.datareader as datareader
import threading
import Barcode.barcode as barcode
import Maxtron.Maxtron_Interface as maxtron
import time as time
import serial

ID = '1'

mensagem_tempo_esgotado = "Tempo de seleção esgotado"
mensagem_selecione_a_maquina = "Selecione a Máquina"
mensagem_selecione_o_produto = "Selecione o Produto"

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
block_minus_plus = False
increment = False
decrement = False

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
                if keyboard_msg == '1':
                    keyboard_msg=''
                    increment = True
                    print("increment")
                if keyboard_msg == '4':
                    keyboard_msg=''
                    decrement = True
                    print("decrement")
            time.sleep(0.1)
        else :
            time.sleep(0.250)
           
            keyboard_msg=''

def checkconnection ():
   
    if not fleetManager.connected:
        fleetManager.disconnect()
        fleetManager.inicializar()
        fleetManager.perfconnect()

    if fleetManager.ping() == True:
        print('Pingou')
        fleetManager.connected=True
    else :
        fleetManager.connected=False
    
        

    
def processo_selecao(pointer, maxsize, array):
    global increment
    global decrement
    global block_minus_plus
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
    if is_number_ascii(str(keyboard_msg))==True: 
        print("Tecla encontrada")
        block_minus_plus=True
        processo_digitacao_teclado(pointer, maxsize, array)
        block_minus_plus=False

    return pointer
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

def enviar_command(tag_maq,tag_produto):
    global keyboard_msg
    print("Maquin: ",(tag_maq))
    print("Produto: ",(tag_produto))
    print("Tipo de missão: ",tag_maq["MissionType"])
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
        match tag_maq["MissionType"]:
            case 1:
                #Comando Simples Pega o tag_maq.DeliveryTag e entrega no tag_produto.Tag
                print("missão tipo 1")
                ret = fleetManager.send_lgv_cmd(tag_maq["DeliveryTag"],tag_produto["Tag"],tag_maq["LGV"],tag_maq["Order_ID"],tag_produto["Order_ID"])
            case 2:
                # Duplo: tag_maq.BufferTag -> tag_maq.SupplyTag, tag_maq.DeliveryTag ->tag_produto.Tag
                #ret = rest.send_rest(fleetManager.FLEET_ADDRES, tag_maq,tag_produto)
                print("missão tipo 2")
                #"Nome":"ABASTECE","Priority": 0,"LGV": -1,"DeliveryTag":3,"SupplyTag":4,"BufferTag":999999,"DisposalTag":10,"MissionType":2,  "Order_ID":101}, 
                ret = rest.send_rest(tag_maq["BufferTag"],tag_maq["SupplyTag"],tag_maq["DeliveryTag"],tag_produto["Tag"],tag_maq["LGV"],tag_maq["Order_ID"],tag_produto["Order_ID"])
            case 3:
                # Duplo: tag_produto.Tag -> tag_maq.SupplyTag, tag_maq.DeliveryTag ->tag_maq.BufferTag  -- abastece antes de coletar e envia para um buffer
                # end_rest(PickUp1,DropOff1,PickUp2,DropOff2,lgv,Order_ID1,Order_ID2):
                print("missão tipo 3")
                ret = rest.send_rest(tag_produto["Tag"],tag_maq["SupplyTag"],tag_maq["DeliveryTag"],tag_maq["BufferTag"],tag_maq["LGV"],tag_maq["Order_ID"],tag_produto["Order_ID"])
                  
            case 4:
                # Comando Simples Pega o tag_produto.Tag e entrega no tag_maq.SupplyTag
                print("missão tipo 4")
                ret = fleetManager.send_lgv_cmd(tag_produto["Tag"],tag_maq["SupplyTag"],tag_maq["LGV"],tag_maq["Order_ID"],tag_produto["Order_ID"])
                
            case 5:
                # Comando Simples Pega o tag_maq.DeliveryTag e entrega no tag_maq.DisposalTag
                #send_lgv_cmd(self,PickUp,DropOff,lgv,Order_ID1,Order_ID2):
                print("missão tipo 5")
                ret = fleetManager.send_lgv_cmd(tag_maq["DeliveryTag"],tag_maq["DisposalTag"],tag_maq["LGV"],tag_maq["Order_ID"],tag_maq["Order_ID"])
            case _:
                main_menu.execute_command('Azul OFF')
                main_menu.execute_command('Verde OFF')
                main_menu.execute_command('Vermelho ON')
                main_menu.clear_display()
                main_menu.write_line1('PROBLEMA')
                main_menu.write_dinamic_line2('PEDIDO NAO REALIZADO')
                time.sleep(10)

                return 
        if not fleetManager.connected:
            fleetManager.disconnect()
            fleetManager.inicializar()
            fleetManager.perfconnect()
    if (ret==True):
        main_menu.execute_command('Azul ON')
        main_menu.execute_command('Verde ON')
        main_menu.execute_command('Vermelho ON')
        main_menu.clear_display()
        main_menu.write_line1('PEDIDO')
        main_menu.write_dinamic_line2('REALIZADO')
        time.sleep(8)
    return


def sel_regiao():
    global keyboard_msg
    global REGIAO
    print("Carrega regiao")
    while True:
        regiao_selecionada =0
        keyboard_msg=''
        main_menu.clear_display()
        time.sleep(0.1)
        region_tot = len(datareader.region_list())
        print("Total de regiões:",len(datareader.region_list()) )
        region_nome = datareader.region_list()
        print("Lista regiao: ",datareader.region_list())
        print("Regiao Selecionada: ",region_nome[regiao_selecionada])
        main_menu.write_line1('Sel Reg.')
        main_menu.write_line2(region_nome[regiao_selecionada])
        while True:
            regiao_selecionada= processo_selecao(regiao_selecionada,region_tot,region_nome)
            if keyboard_msg=='ENT': 
                REGIAO=region_nome[regiao_selecionada]
                #print("Tag: ",datareader.tag_machines(region_nome[regiao_selecionada],region_nome[maquina_selecionada]))  
                print("enter encontrado")
                return REGIAO
                    
            if keyboard_msg =='CLR':
                break
        #if keyboard_msg =='CLR':
        #    break
           
            time.sleep(0.250)
    return 'Falhou'


    return
def pedido_viateclado():
    time.sleep(0.1)
    keyboard_msg=''
    sel_regiao()
    tag_maq = sel_maq()
    print("Tag da maquina: ",(tag_maq))
    time.sleep(0.1)
    try:
        keyboard_msg=''
        
        if tag_maq['MissionType']!=5:
            tag_produto = sel_produto()
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
def sel_produto():
    
    global keyboard_msg
    
    global produto_tot  
    global produtos_bitola

    global produtos_bitola_tot 
    global produtos_bitola_nomes 

    pointer = 0
    regiao_selecionada = pointer
    maquina_selecionada = 0
    
    bitola_selecionada = 0
    subproduto_selecionado = 0
    print ("Processo teclado")
    main_menu.clear_display()
    time.sleep(0.1)
    main_menu.write_line1('Sel.Bito')
    main_menu.write_line2(produtos_bitola[bitola_selecionada])
    while True:
        if barcode_msg != '':
            return prod_scanner()
        bitola_selecionada= processo_selecao(bitola_selecionada,produto_tot,produtos_bitola)
        time.sleep(0.250)
        if keyboard_msg=='ENT':
            produtos_bitola_nomes=datareader.produto_bitola_items(produtos_bitola[bitola_selecionada])
            produtos_bitola_tot=len(produtos_bitola_nomes)
            print("Bitola selecionada ", produtos_bitola[bitola_selecionada])

            main_menu.write_line1('Produto ')
            main_menu.write_line2(produtos_bitola_nomes[0])

            keyboard_msg=''
            while True:
                subproduto_selecionado= processo_selecao(subproduto_selecionado,produtos_bitola_tot,produtos_bitola_nomes)
                time.sleep(0.250)
                if keyboard_msg=='ENT':
                    print("Tag Produto ", datareader.tagproduto(produtos_bitola[bitola_selecionada],produtos_bitola_nomes[subproduto_selecionado]).items())
                   
                    return datareader.tagproduto(produtos_bitola[bitola_selecionada],produtos_bitola_nomes[subproduto_selecionado])
                if keyboard_msg =='CLR':
                    break
        if keyboard_msg =='CLR':
            break
    
def sel_maq():
    global region_nome
    global region_tot
    global REGIAO

    global maquinas_nome
    global maquinas_tot
    global keyboard_msg
    
    pointer = 0
    print("Nome das regiões   ",region_nome)

    regiao_selecionada = region_nome.index(REGIAO)

    maquina_selecionada = 0
    
    
    print ("Processo teclado")

    while True:
        print("Regiao Selecionada: ",region_nome[regiao_selecionada])
        keyboard_msg=''
        main_menu.clear_display()
        time.sleep(0.1)
        maquinas_tot = len(datareader.maq_region_list(region_nome[regiao_selecionada]))
        maquinas_nome = datareader.maq_region_list(region_nome[regiao_selecionada])
        print("Regiao Selecionada: ",maquinas_nome[maquina_selecionada])
        main_menu.write_line1('Sel.Maq.')
        main_menu.write_line2(maquinas_nome[maquina_selecionada])
        while True:
            maquina_selecionada= processo_selecao(maquina_selecionada,maquinas_tot,maquinas_nome)
            if keyboard_msg=='ENT': 
                print("Tag: ",datareader.tag_machines(region_nome[regiao_selecionada],maquinas_nome[maquina_selecionada]))  
                return datareader.tag_machines(region_nome[regiao_selecionada],maquinas_nome[maquina_selecionada])
                    
            if keyboard_msg =='CLR':
                break
        if keyboard_msg =='CLR':
            break
        time.sleep(0.250)
    return 'Falhou'
def pedido_viascanner():
    global barcode_msg
    keyboard_msg=''
    tag_maq =  maq_scanner()
    if tag_maq != 'Falhou':
        if tag_maq['MissionType']==5:
            enviar_command(tag_maq,tag_maq)
            return
        keyboard_msg=''
        tag_produto=prod_scanner()
        if tag_produto == None:
            return
        print("Tag Produto ",tag_produto)
        if tag_maq['MissionType']!=5:
            if tag_produto["Tag"] != 0:
                print("Enviar")
                print("Tag Maq, tag produto",(tag_maq),(tag_produto))
                enviar_command(tag_maq,tag_produto)
                return
            else:
                main_menu.execute_command('Azul ON')
                main_menu.execute_command('Verde ON')
                main_menu.execute_command('Vermelho OFF')
                main_menu.clear_display()
                main_menu.write_line1('OPS!')
                main_menu.write_dinamic_line2('TENTE NOVAMENTE')
                time.sleep(10)
        else:
            print("Maquina para descarte")
            enviar_command(tag_maq,tag_maq)
            return 
    main_menu.write_line1('Maq.    ')
    main_menu.write_line2('Nao Encontrada ')
    time.sleep(5)
    return

def prod_scanner():
    global barcode_msg
    barcode_msg=''
    main_menu.write_line1('Scaneie ')
    main_menu.write_line2('Produto ')
    time.sleep(3)
    while True: 
        if keyboard_msg=='ENT':
            return sel_produto()
        if barcode_msg != '':
            print("Readed Barcode: ",barcode_msg)
            tagproduto=datareader.tagqrcodprod(barcode_msg)
            #nomeProduto=datareader.nomeqrcodprod(barcode_msg)
            print(tagproduto)
            barcode_msg=''
            if tagproduto !=None:
                main_menu.write_line1('Prod.Sel')
                main_menu.write_line2(tagproduto["Nome"])
                time.sleep(3)
                return tagproduto
            else:
                main_menu.write_line1('Produto ')
                main_menu.write_line2('Nao enc.')
                time.sleep(3)
                main_menu.write_line1('Scaneie')
                main_menu.write_line2('Produto')
                time.sleep(1)
            if keyboard_msg =='CLR':
                return 'Falhou'

        
    return 'Falhou'

def maq_scanner():
    global barcode_msg
    print("Processo via scanner")
    if barcode_msg != '':
        print("Readed Barcode: ",barcode_msg)
        tagmaquina=datareader.tagqrcodemaq(str(barcode_msg))
        #nomemaquina=datareader.nomeqrcodemaq(str(barcode_msg))
        
        
        barcode_msg=''
        print(barcode_msg)
        if tagmaquina != None:
            print("tagmaquina ",(tagmaquina))
            main_menu.write_line1('Maq.Sele. ')
            main_menu.write_line2(tagmaquina['Nome'])
            time.sleep(5)
            return tagmaquina
        else:
            print("Maq não encontrada")
            return 'Falhou'
        if keyboard_msg =='CLR':
            return 'Falhou'
    return 'Falhou'


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
    print(len(datareader.region_list()))
    region_tot = len(datareader.region_list())
    region_nome = datareader.region_list()

    produto_tot = len(datareader.produto_bitola_list())
    produtos_bitola = datareader.produto_bitola_list()
    main_menu = maxtron.init()

    config=datareader.config()
 
    REGIAO=config["REGIAO"]

    print("Iniciando")
    t = time.perf_counter()
    fleetManager = server.serverSocket()
    print(config)
    print(config["IP-FLEETMANAGER"],"   ",config["PORT"])
    fleetManager.configure(config["IP-FLEETMANAGER"],config["PORT"])
    fleetManager.inicializar()
    fleetManager.perfconnect()
    #fleetManager.FLEET_ADDRES = datareader.config[1]
    
    #fleetManager.FLEET_PORT =datareader.config[2]
    fleetManager.load_defaults(config["ID"])
    
    

    thread_barcode = threading.Thread(target=read_barcode)
    thread_keyboard = threading.Thread(target=read_keyboard)
    thread_barcode.start()
    thread_keyboard.start()
    while True:
        
        elapsed_time = time.perf_counter() - t
        time.sleep(0.2)
        if(fleetManager.connected ==True):
            if barcode_msg != '':
                pedido_viascanner()

            if keyboard_msg !='':
                if keyboard_msg == 'PUSH':
                    keyboard_msg=''
                    pedido_viateclado()

        if ((time.perf_counter() - t)>(10)):
            t = time.perf_counter()
            checkconnection()
            if(fleetManager.connected ==True):
                print('Conectado')
                gerenciador_encontrado(main_menu)
            else:
                print('Não conectado')
                gerenciador_n_encontrado(main_menu)
                
           
