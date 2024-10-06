import requests
import os
import subprocess,sys
import re
import json

def ativar_eth0_dhcp():
    try:
        # Verifica se o NetworkManager está rodando
        nm_status = subprocess.run(['nmcli', '-t', '-f', 'RUNNING', 'general'], stdout=subprocess.PIPE, text=True)
        if 'running' not in nm_status.stdout:
            print("NetworkManager não está rodando.")
            return

        # Ativa a interface eth0 se estiver desativada
        os.system("nmcli device set eth0 managed yes")
        os.system("nmcli device connect eth0")

        # Configura a eth0 para usar DHCP
        os.system("nmcli connection modify eth0 ipv4.method auto")

        # Sobe a conexão
        os.system("nmcli connection up eth0")

        # Verifica o status da conexão
        status_conexao = subprocess.run(['nmcli', '-t', '-f', 'NAME,TYPE,STATE', 'connection', 'show', '--active'], stdout=subprocess.PIPE, text=True)
        print("Conexões ativas:")
        print(status_conexao.stdout)

    except Exception as e:
        print(f"Erro ao configurar a eth0 para DHCP: {e}")

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
    mascara="24"
    
    try:
        # Verifica se o NetworkManager está rodando
        nm_status = subprocess.run(['nmcli', '-t', '-f', 'RUNNING', 'general'], stdout=subprocess.PIPE, text=True)
        if 'running' not in nm_status.stdout:
            print("NetworkManager não está rodando.")
            return

        # Remove uma conexão existente com o mesmo nome (se houver)
        #os.system(f"nmcli connection delete {config['SSID']}")

        # Cria uma nova conexão Wi-Fi
        os.system(f"nmcli dev wifi connect {config['SSID']} password {config['PASSWORD']}")

        # Define IP estático, máscara e gateway
        os.system(f"nmcli connection modify {config['SSID']} ipv4.addresses {config['IP_ADDRESS']}/{mascara}")
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
    
    ativar_eth0_dhcp()
