import requests
import os
import json
import time as time

class server_response:
    ret = False
    message = "Nao Recebido"


class serverSocket:
    def configure(self, IP, PORT, ID):

        # URL para onde o JSON será enviado
        self.ID = ID
        self.IP = IP
        self.PORT = PORT
        self.CONNECTED = False
        self.sequence = 1
        
    def heartbeat(self):
        #url = 'http://187.102.244.27:8080/v1/button/comm'
             #'http://187.102.244.270:8080/v1/button/comm'
        #self.sequence = 1
        self.connected = True
        
        ret = False
        #url = "http://"+self.IP +":" +str(self.PORT)+"/v1/button/comm"
        url = "http://"+self.IP +":" +str(self.PORT)+"/v1/button/call"
        data = {
                "id_button" :1,
                "message_type" : "LIFE",
                "sequence":0
                }
        data["id_button"] = self.ID
        data["sequence"] = self.sequence
        # Cabeçalhos da requisição, se necessário
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            # Envia o JSON usando o método POST
            response = requests.post(url, json=data, headers=headers)
            #print(data)
            # Verifica se a resposta foi um código 200 (OK)
            if response.status_code == 200:
                # Tenta converter a resposta para JSON
                self.CONNECTED = True
                # Verifica se o item "Recebido" está no JSON e é True
                #try:
                #    resposta_json = response.json()
                #    print("Respondeu")
                #    self.CONNECTED = True
                #except:
                #    print("Erro ao Ler o JSON")
                #    self.CONNECTED = False
                
                
            else:
                #print(f"Erro: Código de status {response.status_code}")
                self.CONNECTED = False
        except requests.exceptions.RequestException as e:
            #print(f"Erro ao enviar requisição: {e}")
            self.CONNECTED = False
        #self.CONNECTED = True
        self.sequence = self.sequence+1
        if (self.sequence) > 2147483647 :
            self.sequence = 1 
            
            

    def send_command(self,maquina,produto):
        #url = 'http://187.102.244.27:8080/v1/button/comm'
        #'http://187.102.244.270:8080/v1/button/comm'
        serverresponse = server_response()
        serverresponse.message = "Nao Recebido"
        serverresponse.ret = False 
        url = "http://"+self.IP +":" +str(self.PORT)+"/v1/button/call"
        data =   {
                "id_button" :1,         
                "message_type" : "ACTION",  
                "material_type": "PALLET",  
                "action_type":"ABASTECE",  
                "situation": "COMPLETO",  
                "id_machine": 1, 
                "sku":"23"
                }
       
        data["id_button"]=self.ID    
        #data["message_type"]=maquina    
        data["material_type"]=produto.material_type
        data["action_type"]=maquina.action_type  
        data["situation"]=maquina.situation 
        data["id_machine"]=maquina.id_machine   
        data["sku"]=str(produto.SKU)
        print(data)
        # Cabeçalhos da requisição, se necessário
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            # Envia o JSON usando o método POST
            response = requests.post(url, json=data, headers=headers)
            
            # Verifica se a resposta foi um código 200 (OK)
            if response.status_code == 200:
                # Tenta converter a resposta para JSON
                resposta_json = response.json()
                print("Reposta do JSON ",resposta_json)
                # Verifica se o item "Recebido" está no JSON e é True
                try:
                   
                    if resposta_json["message"]=="Confirmado!":
                        print("JSON recebido com sucesso e 'Recebido' é True.")
                        serverresponse.ret = True
                        serverresponse.message = resposta_json["message"]
                    else:
                        print("JSON recebido, mas 'Recebido' não é True ou não está presente.")
                        serverresponse.ret = False
                        serverresponse.message = resposta_json["message"]
                except:
                    print("Erro ao Ler o JSON")
                    serverresponse.ret = False
                    serverresponse.message = "Servidor Nao respondeu corretamente"
                
                
            else:
                print(f"Erro: Código de status {response.status_code}")
                serverresponse.ret = False
                serverresponse.message = "Servidor Nao Respondeu"

        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar requisição: {e}")
            serverresponse.ret = False
            serverresponse.message = "Falhou No envio"

        return serverresponse

#def run():
#    heartbeat()
#con = serverSocket()
#con.configure("187.102.244.27","8080",1)
#while True:
   
    #con.send_command()
#    con.heartbeat()
#    time.sleep(3)


    def fetch_and_replace(self, endpoint, output_file):
        url = "http://"+self.IP +":" +str(self.PORT)+endpoint
        try:
            # Fazer requisição HTTP
            response = requests.get(url)
            response.raise_for_status()  # Levantar exceção para erros HTTP

            # Verificar se o retorno é JSON
            data = response.json()  # Lança ValueError se não for JSON

            # Validar o JSON 
            # Exemplo simples: Verificar se o JSON é um dicionário
            if not isinstance(data, dict):
                raise ValueError("O JSON retornado não é um objeto válido.")

            # Salvar o JSON em um arquivo temporário
            temp_file = f"{output_file}.tmp"
            with open(temp_file, 'w', encoding='utf-8') as temp:
                json.dump(data, temp, ensure_ascii=False, indent=4)

            # Substituir o arquivo existente
            os.replace(temp_file, output_file)
            print(f"Arquivo {output_file} atualizado com sucesso.")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar o URL: {e}")
        except ValueError as e:
            print(f"Erro de validação do JSON: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

# Exemplo de uso
#/v1/button/config/qrcodeprod.json
#/v1/button/config/produtos.json
#output_file = "dados.json"  # Caminho do arquivo a ser substituído
#fetch_and_replace("/v1/button/config/qrcodeprod.json", output_file)
#fetch_and_replace("/v1/button/config/produtos.json",output_file0)
