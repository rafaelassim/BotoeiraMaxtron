import os
import subprocess

def criar_conexao_wifi_estatica(ssid, senha, ip_estatico, mascara, gateway, dns):
    try:
        # Verifica se o NetworkManager está rodando
        nm_status = subprocess.run(['nmcli', '-t', '-f', 'RUNNING', 'general'], stdout=subprocess.PIPE, text=True)
        if 'running' not in nm_status.stdout:
            print("NetworkManager não está rodando.")
            return

        # Remove uma conexão existente com o mesmo nome (se houver)
        os.system(f"nmcli connection delete {ssid}")

        # Cria uma nova conexão Wi-Fi
        os.system(f"nmcli dev wifi connect {ssid} password {senha}")

        # Define IP estático, máscara e gateway
        os.system(f"nmcli connection modify {ssid} ipv4.addresses {ip_estatico}/{mascara}")
        os.system(f"nmcli connection modify {ssid} ipv4.gateway {gateway}")
        os.system(f"nmcli connection modify {ssid} ipv4.dns {dns}")
        os.system(f"nmcli connection modify {ssid} ipv4.method manual")  # Desativa DHCP

        # Ativa a nova configuração
        os.system(f"nmcli connection up {ssid}")

        # Verifica o status da conexão
        status_conexao = subprocess.run(['nmcli', '-t', '-f', 'NAME,TYPE,STATE', 'connection', 'show', '--active'], stdout=subprocess.PIPE, text=True)
        print("Conexões ativas:")
        print(status_conexao.stdout)

    except Exception as e:
        print(f"Erro ao tentar configurar a conexão: {e}")

# Exemplo de uso
ssid = "Sleonela"
senha = "azul3878"
ip_estatico = "192.168.0.100"  # IP estático
mascara = "24"  # Máscara (CIDR)
gateway = "192.168.0.1"  # Gateway padrão
dns = "8.8.8.8"  # Servidor DNS

criar_conexao_wifi_estatica(ssid, senha, ip_estatico, mascara, gateway, dns)
