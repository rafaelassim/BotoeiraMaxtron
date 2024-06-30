#import Server.server as server
import Server.server as server
import Barcode.barcode as barcode
import Gerenciador.gerenciador as gerenciador
import DataReader.datareader as datareader
import threading
import Barcode.barcode as barcode
import Maxtron.Maxtron_Interface as maxtron
import time as time
import serial

mensagem_tempo_esgotado = "Tempo de seleção esgotado"
mensagem_selecione_a_maquina = "Selecione a Máquina"
mensagem_selecione_o_produto = "Selecione o Produto"
maquinas_tot = 0
maquinas_nome = []

produto_tot = 0
produtos_bitola = []

produtos_bitola_tot =0
produtos_bitola_nomes =[]

barcode_msg = ''
keyboard_msg = ''

increment = False
decrement = False

def read_barcode():
    global barcode_msg
    global increment
    global decrement
    while True:
        if barcode_msg == '':
            barcode_msg=barcode.read()

        else :
            time.sleep(1)

def read_keyboard():
    global keyboard_msg
    global increment
    global decrement
    increment=False
    decrement=False
    
    print("Iniciando teclado")
    while True:
        if keyboard_msg == '':
            keyboard_msg=main_menu.read_button_press()
            print(keyboard_msg)
            if keyboard_msg == '1':
                keyboard_msg=''
                increment = True
                print("increment")
            if keyboard_msg == '4':
                keyboard_msg=''
                decrement = True
                print("decrement")
        else :
            time.sleep(0.250)
            keyboard_msg=''

def checkconnection ():
    fleetManager.__init__()
    fleetManager.ping()
    fleetManager.disconnect()
    print('Checando conexão')

def processo_selecao(pointer, maxsize, array):
    global increment
    global decrement
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
        main_menu.write_line2(array[pointer])
    return pointer

def enviar_command(maq,destino):
    print("Coletar na tag: ",maq)
    print("Entregar no destino: ",destino)
    return

def pedido_viateclado():
    global maquinas_nome
    global maquinas_tot
    global keyboard_msg
    
    global produto_tot  
    global produtos_bitola

    global produtos_bitola_tot 
    global produtos_bitola_nomes 

    pointer = 0
    maquina_selecionada = pointer
    
    bitola_selecionada = 0
    subproduto_selecionado = 0
    print ("Processo teclado")
    main_menu.clear_display()
    time.sleep(0.1)
    main_menu.write_line1('Sel. Maqui:')
    main_menu.write_line2(maquinas_nome[pointer])

    while True:
        maquina_selecionada= processo_selecao(maquina_selecionada,maquinas_tot,maquinas_nome)
        if keyboard_msg=='ENT':
            keyboard_msg=''
            main_menu.clear_display()
            time.sleep(0.1)
            print("Maquina Selecionada: ",maquinas_nome[maquina_selecionada])
            main_menu.write_line1('Sel.Bito')
            main_menu.write_line2(produtos_bitola[bitola_selecionada])
            while True:
                bitola_selecionada= processo_selecao(bitola_selecionada,produto_tot,produtos_bitola)
                time.sleep(0.250)
                if keyboard_msg=='ENT':
                   produtos_bitola_nomes=datareader.produto_bitola_items(produtos_bitola[bitola_selecionada])
                   produtos_bitola_tot=len(produtos_bitola_nomes)
                   print("Bitola selecionada ", produtos_bitola[bitola_selecionada])

                   main_menu.write_line1('SubProd.')
                   main_menu.write_line2(produtos_bitola_nomes[0])

                   keyboard_msg='keyboard_msg'
                   while True:
                        subproduto_selecionado= processo_selecao(subproduto_selecionado,produtos_bitola_tot,produtos_bitola_nomes)
                        time.sleep(0.250)
                        if keyboard_msg=='ENT':
                            print("SubProduto Selecionado ", produtos_bitola_nomes[subproduto_selecionado])
                            print("selecionado maquina, bitola e subproduto")
                            enviar_command(datareader.tag_machines(maquinas_nome[maquina_selecionada]),datareader.tag_produto(produtos_bitola[bitola_selecionada],produtos_bitola_nomes[subproduto_selecionado]))
                            return
                        if keyboard_msg =='CLR':
                            break
                if keyboard_msg =='CLR':
                    break
            #pointer= processo_selecao(pointer,maquinas_tot,maquinas_nome)
            if keyboard_msg =='CLR':
                break
        
        if keyboard_msg =='CLR':
            break
        time.sleep(0.250)
    return

def pedido_viascanner():
    global barcode_msg
    tagproduto=''
    nomeProduto =''

    tagmaquina=''
    nomemaquina=''

    print("Lido Pelo Scanner: ",barcode_msg)
    tagproduto=datareader.tagqrcodprod(barcode_msg)
    nomeProduto=datareader.nomeqrcodprod(barcode_msg)
    barcode_msg =''
    print(tagproduto)
    print(nomeProduto)
    if tagproduto !=None:
        main_menu.write_line1('Prod.Sele.')
        main_menu.write_line2(nomeProduto)
        time.sleep(3)
        if keyboard_msg =='CLR':
            return 
        main_menu.write_line1('Scaneie')
        main_menu.write_line2('Maq.  ')
        time.sleep(3)
        barcode_msg =''
        while True: 
            if barcode_msg != '':
                print("Readed Barcode: ",barcode_msg)
                tagmaquina=datareader.tagqrcodemaq(barcode_msg)
                nomemaquina=datareader.nomeqrcodemaq(barcode_msg)
                barcode_msg=''
                if tagmaquina !=None:
                    main_menu.write_line1('Maq.Sele. ')
                    main_menu.write_line2(nomemaquina)
                    time.sleep(3)
                    enviar_command(tagmaquina,tagproduto)
                    return
                else :
                    break
            if keyboard_msg =='CLR':
                break

    return

def envia_mensagem(main_menu):
    global total_connections
    readed_value =[]
    gerenciador_proc_message(main_menu)
    print("Scanneie a Máquina")
    main_menu.write_line1('SCANEIE ')
    main_menu.write_line2('A MAQ.   ')
    product = barcode.read()
    if len(product) <= 2:
        total_connections =99
        print("Esgotou o Tempo de leitura")
        return False
    print("Scanneie o Produto")
    main_menu.write_line1('SCANEIE ')
    main_menu.write_line2('O PRODU.')
    machine = barcode.read()
    if len(machine) <= 2:
        total_connections =99
        print("Esgotou o Tempo de leitura")
        return False
    gerenciador.product = product
    #gerenciador.generate_machine(machine)
    #gerenciador.generate_machine(gerenciador.string_to_list_bytes(machine))
    gerenciador.machine_selected = machine
    total_connections =99
    main_menu.write_line1('ENVIANDO')
    main_menu.write_line2('AGUARDE ')
    
    main_menu.execute_command('Azul ON')
    main_menu.execute_command('Verde ON')
    while gerenciador.machine_selected==machine:
        time.sleep(1)
    return True

def gerenciador_encontrado(main_menu):
    main_menu.execute_command('Azul OFF')
    main_menu.execute_command('Verde ON')
    main_menu.execute_command('Vermelho OFF')
    main_menu.clear_display()
    main_menu.write_line1('TUNKERS ')
    main_menu.write_line2('BOTOEIRA')
    time.sleep(0.1)

def gerenciador_n_encontrado(main_menu):
    main_menu.execute_command('Azul OFF')
    main_menu.execute_command('Verde OFF')
    main_menu.execute_command('Vermelho ON')
    #main_menu.clear_display()
    main_menu.write_line1('BOTOEIRA ')
    main_menu.write_dinamic_line2('Sem Conex.  ')
    time.sleep(0.1)

def gerenciador_proc_message(main_menu):
    main_menu.execute_command('Azul ON')
    main_menu.execute_command('Verde OFF')
    main_menu.execute_command('Vermelho OFF')


if __name__ == '__main__':
      
    global total_connections
    print(len(datareader.machines_list()))
    maquinas_tot = len(datareader.machines_list())
    maquinas_nome = datareader.machines_list()

    produto_tot = len(datareader.produto_bitola_list())
    produtos_bitola = datareader.produto_bitola_list()
    main_menu = maxtron.init()

    #main_menu.run()        
    #server.run()
    fleetManager = server.serverSocket()
    print("Iniciando")
    t = time.perf_counter()
    fleetManager.perfconnect()
    fleetManager.disconnect()
    thread_barcode = threading.Thread(target=read_barcode)
    thread_keyboard = threading.Thread(target=read_keyboard)
    thread_barcode.start()
    thread_keyboard.start()
    while True:
        
        elapsed_time = time.perf_counter() - t
        time.sleep(0.2)
        
        if barcode_msg != '':
            pedido_viascanner()


        if keyboard_msg !='':
            if keyboard_msg == 'PUSH':
                keyboard_msg=''
                pedido_viateclado()
                gerenciador_encontrado(main_menu)

        if ((time.perf_counter() - t)>(10)):
            t = time.perf_counter()
            checkconnection()
            if(fleetManager.connected ==True):
                print('Conectado')
                gerenciador_encontrado(main_menu)
            else:
                print('Não conectado')
                gerenciador_n_encontrado(main_menu)
                
           

#
def old():
    server.run(gerenciador)
    gerenciador_n_encontrado(main_menu)
    total_connections = 99
    
    while True:
            button_press = main_menu.read_button_press()
            
            if server.total_connections == 1 :
                if button_press == '1':
                    envia_mensagem(main_menu)
            
            if total_connections != server.total_connections:
                total_connections=server.total_connections
                
                if server.total_connections == 1 :
                    gerenciador_encontrado(main_menu)
                else:
                    gerenciador_n_encontrado(main_menu)
                         #button_press = main_menu.read_button_press()
        ##print(f"Machine Selection - Button pressed: {button_press}")  # Debugging print
        
              #  gerenciador_encontrado(main_menu)
           
              #  gerenciador_n_encontrado(main_menu)
    #gerenciador.blink_heart_beat()
    print("Entre com o valor do Scanner")
    #lista = gerenciador.string_to_list_bytes(input())

   # gerenciador.data_from_scanner=lista
    #gerenciador.data_from_scanner=gerenciador.string_to_list_bytes( barcode.read())
    gerenciador.product=barcode.read()
    print(gerenciador.product)
    time.sleep(1)
    print("Entre com a máquina selecionada")
    #lista = gerenciador.string_to_list_bytes(barcode.read())
    gerenciador.generate_machine(input())
    gerenciador.control_bytes = [0x00,0x01,0x02,0x03,0x04]
    #gerenciador.generate_machine(barcode.read())
    print(gerenciador.machine_selected)
    
  
    #server.run(gerenciador)
    print('Finalizado Inicio')