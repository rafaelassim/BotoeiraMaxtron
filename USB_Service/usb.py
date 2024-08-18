import os
import time
import pyudev
import shutil
import subprocess

# Configurações
MOUNT_DIR = "/mnt/usb"
DEST_DIR = "/home/tunkers/BotoeiraMaxtron"
FOLDER_NAME = "update"

def mount_device(device_path):
    if not os.path.exists(MOUNT_DIR):
        os.makedirs(MOUNT_DIR)
    subprocess.run(["sudo", "mount", device_path, MOUNT_DIR], check=True)

def unmount_device():
    subprocess.run(["sudo", "umount", MOUNT_DIR], check=True)

def copy_files(main_menu):
    source_folder = os.path.join(MOUNT_DIR, FOLDER_NAME)
    if os.path.exists(source_folder):
        print(f"Pasta '{FOLDER_NAME}' encontrada. Iniciando cópia...")
        shutil.copytree(source_folder, DEST_DIR, dirs_exist_ok=True)
        print("Cópia concluída.")
        main_menu.clear_display()
        main_menu.execute_command('Azul ON')
        main_menu.execute_command('Verde OFF')
        main_menu.execute_command('Vermelho OFF')
        time.sleep(1)
        main_menu.write_line1('REINICIE')
        main_menu.write_dinamic_line2('A BOTOEIRA')
        while True:
            time.sleep(3)
            main_menu.clear_display()
            main_menu.execute_command('Azul ON')
            main_menu.execute_command('Verde ON')
            main_menu.execute_command('Vermelho ON')
            time.sleep(1)
            main_menu.write_line1('REINICIE')
            main_menu.write_dinamic_line2('A BOTOEIRA')
    else:
        print(f"Pasta '{FOLDER_NAME}' não encontrada.")

def monitor_usb(main_menu):
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block')
    monitor.start()

    for device in iter(monitor.poll, None):
        if device.action == 'add' and "sd" in device.device_node:
            device_path = device.device_node
            print(f"Dispositivo USB detectado: {device_path}")
            try:
                mount_device(device_path)
                print(f"Dispositivo montado em {MOUNT_DIR}")
                copy_files(main_menu)
            except subprocess.CalledProcessError:
                print("Falha ao montar o dispositivo.")
            finally:
                unmount_device()
                print("Dispositivo desmontado.")

if __name__ == "__main__":
    print("Monitorando dispositivos USB...")
    monitor_usb()