import os.path
import os
import time as time


path_files = '/mnt/tunkers/update'
path = '/dev/sdb'
os.system("ls /dev")
while True:
    check_file = os.path.exists(path)
    stream = os.popen('echo Returned output')
    output = stream.read()
    output

    print(check_file)
    time.sleep(2)

def mount_sda:
    os.system("mount /dev/sda  /mnt")

def mount_sda1:
    os.system("mount /dev/sda1 /mnt")

def check_folders:
    check_file = os.path.exists(path_files)
    return check_file

def update_files:
    os.system("cp -r -y path_files ....")

def update_network:
    os.system("/etc/wpa_supplicant/wpa_supplicant.conf   cat /etc/dhcpcd.conf ")