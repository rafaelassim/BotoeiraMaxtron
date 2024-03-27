import Server.server as server
import Barcode.barcode as barcode
import Gerenciador.gerenciador as gerenciador
import threading
import Barcode.barcode as barcode
import Maxtron.Maxtron_Interface as maxtron
import time as time
#import struct

mensagem_tempo_esgotado = "Tempo de seleção esgotado"
mensagem_selecione_a_maquina = "Selecione a Máquina"
mensagem_selecione_o_produto = "Selecione o Produto"


class display():
    def escreve_display (mensagem):
        print(mensagem)
        print(teste)

    def limpa_display():
        print("NULL teste")



def escreve_display (mensagem):
    print(mensagem)

def menu_principal ():
    data_from_scanner = []
    data_from_scanner = barcode.read()
    #gerenciador.data_from_scanner=barcode.read()
    #processa a requisição
    #

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
    
    main_menu = maxtron.init()
    main_menu.clear_display()
    server.run(gerenciador)
    gerenciador_n_encontrado(main_menu)
    while True:
            button_press = main_menu.read_button_press()
            print('button_press',button_press)
            if button_press == 'F1':
                print('main_menu.navigate_up()')
            elif button_press == 'F2':
                print('main_menu.navigate_down()')
            elif button_press == 'ENT':
                print('main_menu.select_item()')
            elif button_press == 'F4':
                pass
            print('Looping')
            #if server.total_connections == 1 :
            #    gerenciador_encontrado(main_menu)
            #else:
            #    gerenciador_n_encontrado(main_menu)
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
    