import Server.server as server
import Barcode.barcode as barcode
import Gerenciador.gerenciador as gerenciador
import threading
import Barcode.barcode as barcode
import Maxtron.Maxtron_Interface as maxtron
import time as time

mensagem_tempo_esgotado = "Tempo de seleção esgotado"
mensagem_selecione_a_maquina = "Selecione a Máquina"
mensagem_selecione_o_produto = "Selecione o Produto"



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
    main_menu.clear_display()
    main_menu.write_line1('BOTOEIRA ')
    main_menu.write_dinamic_line2('Sem Conex.  ')
    time.sleep(0.1)

def gerenciador_proc_message(main_menu):
    main_menu.execute_command('Azul ON')
    main_menu.execute_command('Verde OFF')
    main_menu.execute_command('Vermelho OFF')


if __name__ == '__main__':
    
    global total_connections
    main_menu = maxtron.init()
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
    