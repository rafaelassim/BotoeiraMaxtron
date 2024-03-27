import time
import serial

class Maxtron():
    def __init__(self, serial_port, commands, menu_items):
        self.serial = serial_port
        self.commands = commands
        self.menu_items = menu_items
        self.current_item_index = 0
    
    def run(self):
        self.display_current_item()

        #elf.execute_command('Azul OFF')
        #self.execute_command('Verde OFF')
        #self.execute_command('Vermelho OFF')
        self.execute_command('Azul ON')
        self.clear_display()
        self.write_line1('Iniciando Aguarde... ')
        while True:
            button_press = self.read_button_press()

            if button_press == 'F1':
                self.navigate_up()
            elif button_press == 'F2':
                self.navigate_down()
            elif button_press == 'ENT':
                self.select_item()
            elif button_press == 'F4':
                pass

    def read_button_press(self):
        data = self.serial.read(1)
        return {
            b'0': '0', b'1': '1', b'2': '2', b'3': '3', b'4': '4', b'5': '5', 
            b'6': '6', b'7': '7', b'8': '8', b'9': '9', b'A': 'F1', b'B': 'F2', 
            b'C': 'F3', b'D': 'F4', b'E': 'CLR', b'F': 'ENT'
        }.get(data, None)

    def clear_display(self):
        print("apagando")
        self.execute_command('Array_Apaga_L1')
        print("apagando 2")
        self.execute_command('Array_Apaga_L2')
    
    def clear_l1(self):
        self.execute_command('Array_Apaga_L1')
        
    def clear_l2(self):
        self.execute_command('Array_Apaga_L2')
    
    def execute_command(self, command):
        self.serial.write(self.commands[command])        
        time.sleep(0.25)
    
    def write(self, command):
        self.serial.write(command)
        time.sleep(0.25)

    def write_line1(self, message):
        init_message =  b'\x02\x31\x31\x30\x30\x30'
        end_message =   b'\x03'
        command = init_message +ord(message) + end_message
        self.write(command)
        
    def write_line2(self, message):  
        init_message =  b'\x02\x32\x31\x30\x30\x30'
        end_message =   b'\x03'
        decoded_message= bytes(message,'utf-8')
        command = init_message +decoded_message  + end_message
        self.write(command)
    
    def write_dinamic_line1(self, message):
        init_message =  b'\x02\x31\x31\x30\x30\x31'
        end_message =   b'\x03'
        command = init_message +ord(message) + end_message
        self.write(command)
        
    def write_dinamic_line2(self, message):  
        init_message =  b'\x02\x32\x31\x30\x30\x31'
        end_message =   b'\x03'
        decoded_message= bytes(message,'utf-8')
        command = init_message +decoded_message  + end_message
        self.write(command)
       
        
if __name__ == "__main__":
    ser = serial.Serial('/dev/serial0', baudrate=9600,
    #ser = serial.Serial('/dev/ttyUSB0', baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)

    commands = {
        'Array_Apaga_L1': b'\x02\x31\x31\x30\x30\x30\x20\x20\x20\x20\x20\x20\x20\x20\x03',
        'Array_Apaga_L2': b'\x02\x32\x31\x30\x30\x30\x20\x20\x20\x20\x20\x20\x20\x20\x03',
        'Array_Texto_TUNKERS': b'\x02\x32\x31\x30\x30\x30\x54\x55\x4E\x4B\x45\x52\x53\x20\x03',
        'Array_Apaga_Array_I': b'\x02\x32\x31\x30\x30\x30\x20\x03',
        'Array_Apaga_Array_B': b'\x02\x32\x32\x30\x30\x30\x20\x03',
        'Array_Apaga_Array_O': b'\x02\x32\x33\x30\x30\x30\x20\x03',
        'Array_Apaga_Array_P': b'\x02\x32\x34\x30\x30\x30\x20\x03',
        'Array_I': b'\x02\x32\x31\x30\x30\x30\x49\x03',
        'Array_B': b'\x02\x32\x32\x30\x30\x30\x2f\x03',
        'Array_O': b'\x02\x32\x33\x30\x30\x30\x4f\x03',
        'Array_P': b'\x02\x32\x34\x30\x30\x30\x3a\x03',
        'S1 ON': b'\x02\x33\x30\x30\x31\x31\x03',
        'Liga S2': b'\x02\x33\x30\x30\x32\x31\x03',
        'Vermelho ON': b'\x02\x33\x30\x30\x33\x31\x03',
        'Sel. SKUs': b'\x02\x33\x30\x30\x36\x30\x03',
        'Verde ON': b'\x02\x33\x30\x30\x34\x31\x03',
        'Azul ON': b'\x02\x33\x30\x30\x35\x31\x03',
        'Buzzer ON': b'\x02\x33\x30\x30\x36\x31\x03',
        'Array_Desliga_S1': b'\x02\x33\x30\x30\x31\x30\x03',
        'Array_Desliga_S2': b'\x02\x33\x30\x30\x32\x30\x03',
        'Vermelho OFF': b'\x02\x33\x30\x30\x33\x30\x03',
        'Verde OFF': b'\x02\x33\x30\x30\x34\x30\x03',
        'Azul OFF': b'\x02\x33\x30\x30\x35\x30\x03',
        'Buzzer OFF': b'\x02\x33\x30\x30\x36\x30\x03',
        'Solicita_Leitura': b'\x02\x35\x30\x03',
        'Solicita_ST_Pulsador': b'\x02\x35\x35\x03',
        'Solicita_ST_ENT': b'\x02\x36\x36\x03',
    }
    
    menu_items_prod = [
        "SEL.MAQ."
    ]

    menu_items = [
        "Sel. Maquina",
        "S1 ON",
        "Sel. SKUs",
        "Buzzer ON",
        "Buzzer OFF",
        "Liga S2",
        "Vermelho ON",
        "Verde ON",
        "Azul ON",
        "S1 OFF",
        "S2 OFF",
        "Vermelho OFF",
        "Verde OFF",
        "Azul OFF",
        "Le o estado das 2 entradas, das 2 saidas e do pulsador",
        "Aguarda a leitura da Entrada 1",
        "Aguarda a leitura da Entrada 2",
        "Aguarda a leitura do Pulsador",
        "Escreve/apaga TUNKERS na linha 2 do LCD",
        "Escreve/apaga I/O: na linha2, 4 colunas do LCD",
        "Le o estado Flag ENT e reseta (Call back)",
        "Le o estado Flag Pulsador e reseta (Call back)"
    ]
    
    test_commands = [
        b'\x021100 BITOLA\x03',  # Adjust starting column for BITOLA
        b'\x021100 PRODUTO\x03',  # Adjust starting column for PRODUTO
        b'\x0211000Testbasic\x03',  # Basic command with more text
        b'\x0221000Test line2\x03',  # Changing to line 2
        b'\x02\x31\x32\x30\x30\x30\x54\x65\x73\x74\x20\x20\x20\x20\x03',  # Starting at column 2
        b'\x02\x31\x33\x30\x30\x30\x54\x65\x73\x74\x20\x20\x20\x20\x03',  # Starting at column 3
        b'\x02\x31\x34\x30\x30\x30\x54\x65\x73\x74\x20\x20\x20\x20\x03',   # Starting at column 4
        b'\x02\x31\x35\x30\x30\x30\x54\x65\x73\x74\x20\x20\x20\x20\x03',   # Starting at column 6
        b'\x0215000Test column5\x03',  # Starting at column 5
        b'\x0211000Test  pad\x03'   # Test text with padding
    ]

        
    main_menu = Maxtron(ser, commands, menu_items_prod)
    print("tudo carregado")
    main_menu.execute_command('Azul ON')
    main_menu.clear_display()
    main_menu.write_dinamic_line2('teste  eeeeeeeeeeeeeeeedsdsds')
    #print((bytes("teste", 'ascii')))
   # print(b'\x02\x32\x31\x30\x30\x30\x54\x55\x4E\x4B\x45\x52\x53\x20\x03')
   # for test_command in test_commands:
   #     main_menu.send_test_command(test_command)
   #     time.sleep(2)  # Add a delay to observe each command's effect on the display
    
    #main_menu.run()