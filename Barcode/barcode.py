import keyboard
import time

#keypressed = []
keypressed = ''
had_signal_to_process = False
max_retries = 20

def on_release(event):
    global keypressed
    try:
        keypressed=keypressed+event.name
        print(event.name)
    except:
        print("Fora da tabela Ascii")

def loop_control():
    global had_signal_to_process
    global keypressed
    retries = 0
    while True:
        
        #if len(keypressed)>0:
        if  keypressed !='' :
            time.sleep(0.5)
            had_signal_to_process = True
            
            break
        else:
            time.sleep(1)
        retries +=1
        if retries > max_retries:
            had_signal_to_process
            break
            
def read():
    global keypressed
    #keypressed.clear()
    keypressed=''
    had_signal_to_process = False
    keyboard.on_release(on_release)
    loop_control()
    keyboard.unhook_all()
   
#    n = len(keypressed)
#    for i in range (n):
 #       control_keys[i] = keypressed[i]
    
    return (keypressed)

#input('Pressione Enter para parar\n')
#print (keypressed)
#keyboard.unhook_all()
