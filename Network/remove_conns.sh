#!/bin/bash


# Listar todas as conexões e remover cada uma delas
for conn in $(nmcli -t -f NAME con show)
do
    nmcli con delete "$conn"
    echo "Conexão '$conn' removida."
done

echo "Todas as configurações de rede foram removidas."
