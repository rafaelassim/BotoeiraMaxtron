import subprocess

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

# Executa a função
apagar_conexoes_wifi()