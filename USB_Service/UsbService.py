import os.path
import os
import time as time


path_files = '/mnt/tunkers/update'
path = '/dev/sda'
pathPrimary = '/dev/sda1'
os.system("ls /dev")
while True:
    check_file = os.path.exists(path)
    if check_file :
        mount_sda()

    stream = os.popen('echo Returned output')
    output = stream.read()
    output

    print(check_file)
    time.sleep(2)

def mount_sda:
    if os.path.exists(pathPrimary):
        os.system("mount /dev/sda1  /mnt")
    else :
        os.system("mount /dev/sda  /mnt")

def mount_sda1:
    os.system("mount /dev/sda1 /mnt")

def check_folders:
    check_file = os.path.exists(path_files)
    return check_file

def update_files:
    os.system("cp -r -y path_files ....")

def update_network:
    os.system("/etc/dhcp/dhclient.conf   cat /etc/dhcpcd.conf ")

interface wlan0
static ip_address=192.168.1.90
static routers=192.168.1.1
#static domain_name_servers=[dns-address]

sudo nmcli connection modify "wlan0" \
ipv4.method "manual" \
ipv4.addresses "192.168.1.90/24" 

