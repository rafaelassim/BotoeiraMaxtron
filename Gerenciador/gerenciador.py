import requests
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
        
    def heartbeat(self):
        #url = 'http://187.102.244.27:8080/v1/button/comm'
             #'http://187.102.244.270:8080/v1/button/comm'
        sequence = 1
        self.connected = True
        
        ret = False
        url = "http://"+self.IP +":" +str(self.PORT)+"/v1/button/comm"
        data = {
                "id_button" :1,
                "message_type" : "LIFE",
                "sequence":0
                }
        data["id_button"] = self.ID
        data["sequence"] = sequence
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
                resposta_json = response.json()
                #print(resposta_json)
                # Verifica se o item "Recebido" está no JSON e é True
                try:
                    if data["Último Chamado"] is True:
                        #print("JSON recebido com sucesso e 'Recebido' é True.")
                        self.CONNECTED = True
                    else:
                        #print("JSON recebido, mas 'Recebido' não é True ou não está presente.")
                        self.CONNECTED = True
                except:
                    #print("Erro ao Ler o JSON")
                    self.CONNECTED = False
                
                self.CONNECTED = True
            else:
                #print(f"Erro: Código de status {response.status_code}")
                self.CONNECTED = False
        except requests.exceptions.RequestException as e:
            #print(f"Erro ao enviar requisição: {e}")
            self.CONNECTED = False
        sequence = sequence+1
        if (sequence) > 2147483647 :
            sequence = 1 
            
            

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
                "gauge": "0.8",   
                "product":"0.8 BE14" 
                }
       
        data["id_button"]=self.ID    
        #data["message_type"]=maquina    
        data["material_type"]=maquina.material_type
        data["action_type"]=maquina.action_type  
        data["situation"]=maquina.situation 
        data["id_machine"]=maquina.id_machine   
        data["gauge"]=produto.gauge
        data["product"]=produto.product  
         
        
        # Cabeçalhos da requisição, se necessário
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            # Envia o JSON usando o método POST
            response = requests.post(url, json=data, headers=headers)
            print(data)
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
                    serverresponse.message = resposta_json["message"]
                
                
            else:
                print(f"Erro: Código de status {response.status_code}")
                serverresponse.ret = False
                serverresponse.message = "Servidor Nao Respondeu"

        except requests.exceptions.RequestException as e:
            print(f"Erro ao enviar requisição: {e}")
            serverresponse.ret = False
            serverresponse.message = "Falhou No envio"

        return serverresponse

def run():
    heartbeat()


#con = serverSocket()
#con.configure("187.102.244.27","8080",1)
#con.send_command()
#con.heartbeat()

