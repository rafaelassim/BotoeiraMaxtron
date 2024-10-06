import requests
import os
import subprocess,sys
import re
import json

def apagar_conexoes_wifi():
    try:
        # Lista todas as conexões salvas
        conexoes_salvas = subprocess.run(['nmcli', '-t', '-f', 'NAME,TYPE', 'connection', 'show'], stdout=subprocess.PIPE, text=True)
        conexoes = conexoes_salvas.stdout.splitlines()

        # Filtra e apaga apenas conexões Wi-Fi
        for conexao in conexoes:
            nome, tipo = conexao.split(':')
            print(f"Apagando conexão Wi-Fi: {nome}")
            subprocess.run(['nmcli', 'connection', 'delete', nome])

            if tipo == "wifi":
                print(f"Apagando conexão Wi-Fi: {nome}")
                
        print("Todas as conexões Wi-Fi foram apagadas.")

    except Exception as e:
        print(f"Erro ao tentar apagar conexões Wi-Fi: {e}")

def criar_conexao_wifi_estatica(config):
  
    template=template.replace("@PASSWORD",config['PASSWORD'])
    
   
    template=template.replace("@DNS",config['DNS'])
    try:
        # Verifica se o NetworkManager está rodando
        nm_status = subprocess.run(['nmcli', '-t', '-f', 'RUNNING', 'general'], stdout=subprocess.PIPE, text=True)
        if 'running' not in nm_status.stdout:
            print("NetworkManager não está rodando.")
            return

        # Remove uma conexão existente com o mesmo nome (se houver)
        os.system(f"nmcli connection delete {config['SSID']}")

        # Cria uma nova conexão Wi-Fi
        os.system(f"nmcli dev wifi connect {config['SSID']} config['PASSWORD']")

        # Define IP estático, máscara e gateway
        os.system(f"nmcli connection modify {config['SSID']} ipv4.addresses {config['IP_ADDRESS']}/{"24"}")
        os.system(f"nmcli connection modify {config['SSID']} ipv4.gateway {config['GATEWAY']}")
        os.system(f"nmcli connection modify {config['SSID']} ipv4.dns {config['DNS']}")
        os.system(f"nmcli connection modify {config['SSID']} ipv4.method manual")  # Desativa DHCP

        # Ativa a nova configuração
        os.system(f"nmcli connection up {config['SSID']}")

        # Verifica o status da conexão
        status_conexao = subprocess.run(['nmcli', '-t', '-f', 'NAME,TYPE,STATE', 'connection', 'show', '--active'], stdout=subprocess.PIPE, text=True)
        print("Conexões ativas:")
        print(status_conexao.stdout)

    except Exception as e:
        print(f"Erro ao tentar configurar a conexão: {e}")


def initnetwork(config):

    
    try:
        apagar_conexoes_wifi()
        criar_conexao_wifi_estatica(config)
    except:
        print("Rede não pode ser configurada")
