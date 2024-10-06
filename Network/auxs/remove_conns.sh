#!/bin/bash
string='My long string'
if [[ $string == *"My long"* ]]; then
  echo "It's there!"
fi

wire='connection'
# Listar todas as conexões e remover cada uma delas
for conn in $(nmcli -t -f NAME connection show)
do
    #nmcli con delete "$conn"
    echo "Conexão '$conn' removida."
done

echo "Todas as configurações de rede foram removidas."


# Listar todas as conexões e remover cada uma delas
for conn in $(nmcli -t -f NAME con show)
do
    #if [ "$conn" == *"$wire"* ]; then
    #    echo "Achei" 
    #else 
    #    echo $conn
    #fi
#    nmcli con delete "$conn"
    echo "Conexão '$conn' removida."
done

echo "Todas as configurações de rede foram removidas."
