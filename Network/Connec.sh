#!/bin/bash

CONNECTION_NAME="minha-conexao-wifi"
INTERFACE_NAME="wlp1s0"
SSID="Sleonela"
PASSWORD="azul3878"
IP_ADDRESS="192.168.1.100/24"
GATEWAY="192.168.1.1"
DNS="8.8.8.8"

#!/bin/bash
# Verifique se o nmcli está instalado
if ! command -v nmcli &> /dev/null
then
    echo "nmcli não está instalado. Instale o NetworkManager."
    exit 1
fi

# Adicionar uma nova conexão Wi-Fi
nmcli dev wifi con $SSID password $PASSWORD ifname $INTERFACE_NAME

# Modificar a conexão para usar um endereço IP estático
nmcli con mod $SSID ipv4.addresses $IP_ADDRESS
nmcli con mod $SSID ipv4.gateway $GATEWAY
nmcli con mod $SSID ipv4.dns $DNS
nmcli con mod $SSID ipv4.method manual

# Ativar a nova conexão
nmcli con up $SSID

echo "Configuração da rede Wi-Fi concluída com sucesso."