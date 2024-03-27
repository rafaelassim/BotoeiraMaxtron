import Server.server as server
import Barcode.barcode as barcode
import Gerenciador.gerenciador as gerenciador
import threading
import Barcode.barcode as barcode
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



if __name__ == '__main__':
 
    time.sleep(1)
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
    
  
    server.run(gerenciador)
    print('Finalizado Inicio')
    