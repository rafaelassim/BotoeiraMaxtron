import keyboard
import time

keypressed = []
had_signal_to_process = False
max_retries = 20

def on_release(event):
    keypressed.append(ord(event.name))
    print(event.name)

def loop_control():
    global had_signal_to_process
    retries = 0
    while True:
        
        if len(keypressed)>0:
            time.sleep(0.5)
            had_signal_to_process = True
            print('pressed ',keypressed)
            break
        else:
            time.sleep(1)
        retries +=1
        if retries > max_retries:
            had_signal_to_process
            break
            
def read():
    keypressed.clear()
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
