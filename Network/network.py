import requests
import os
import subprocess,sys
import re
import json


def initnetwork(config):


    with open("/home/tunkers/BotoeiraMaxtron/Network/connection.txt", "r") as arquivo:
        template = arquivo.read()    

    #template=template.replace("@INTERFACE_NAME",config['INTERFACE_NAME'])
    template=template.replace("@INTERFACE_NAME",'preconfigured')
    template=template.replace("@SSID",config['SSID'])
    template=template.replace("@PASSWORD",config['PASSWORD'])
    template=template.replace("@IP_ADDRESS",config['IP_ADDRESS'])
    template=template.replace("@GATEWAY",config['GATEWAY'])
    template=template.replace("@DNS",config['DNS'])
    try:
        result = subprocess.check_output(template, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)

    except subprocess.CalledProcessError as cpe:
        result = cpe.output
        print("Não foi configurado")
    print(template)
