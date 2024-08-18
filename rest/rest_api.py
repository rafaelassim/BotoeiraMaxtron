import requests
import os
import subprocess,sys
import re
import json

from requests.auth import HTTPBasicAuth

def send_json_nousername(url, data):
    try:
        # Enviando o JSON para a URL usando o método POST
        response = requests.post(url, json=data)
        
        # Verificando se a resposta foi recebida corretamente (status code 2xx)
        if response.status_code // 100 == 2:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        # Imprimindo o erro em caso de exceção
        print(f"Ocorreu um erro: {e}")
        return False


def send_json(url, data, username, password):
    try:
        # Enviando o JSON para a URL usando o método POST com autenticação básica
        response = requests.post(url, json=data, auth=HTTPBasicAuth(username, password))
        
        # Verificando se a resposta foi recebida corretamente (status code 2xx)
        if response.status_code // 100 == 2:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        # Imprimindo o erro em caso de exceção
        print(f"Ocorreu um erro: {e}")
        return False

def send_rest(PickUp1,DropOff1,PickUp2,DropOff2,lgv,Order_ID1,Order_ID2):

  with open("/home/rafael/Documentos/Projetos/Python/BotoeiraMaxtron/rest/rest_apy.txt", "r") as arquivo:
    template = arquivo.read()    

  text ="INICIO"
  try:
    result = subprocess.check_output(template, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)

  except subprocess.CalledProcessError as cpe:
    result = cpe.output

  finally:  
    for line in result.splitlines():
      #print(line.decode())
      text = text+ line.decode() 
  
  json_pattern = re.search(r'\{.*?\}', text)

  if json_pattern:
    # Parse the JSON part
    json_string = json_pattern.group(0)
    data = json.loads(json_string)

    # Extrair o access_token
    access_token = data["access_token"]

    print(access_token)
  else:
    access_token ="fff"
    print("JSON não encontrado na string.")   
  
        # Enviando o JSON para a URL usando o método POST com autenticação básica
    #Abrindo o arquivo template
  with open("/home/tunkers/BotoeiraMaxtron/rest/curl.txt", "r") as arquivo:
  
	  template = arquivo.read()    
        # Verificando se a resposta foi recebida corretamente (status code 2xx)

  template=template.replace("@APIKEY",str(access_token))

  template=template.replace("@ID1",str(Order_ID1))
  template=template.replace("@ID2",str(Order_ID2))
  template=template.replace("@Dropoff2",str(DropOff2))
  template=template.replace("@Pickup2",str(PickUp2))
  template=template.replace("@Dropoff1",str(DropOff1))
  template=template.replace("@Pickup1",str(PickUp1))
  print("Enviando via script")
  print(template)
  try:
    result = subprocess.check_output(template, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)

  except subprocess.CalledProcessError as cpe:
    result = cpe.output

  finally:  
    for line in result.splitlines():
      print(line.decode())
      if 'Mission Created Succesfully' in line.decode():
        print("ok")
        return True
    
  return False

  
def replace_ids(json_data, new_ids, id_index=0):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == 'Id' and id_index < len(new_ids):
                json_data[key] = new_ids[id_index]
                id_index += 1
            else:
                id_index = replace_ids(value, new_ids, id_index)
    elif isinstance(json_data, list):
        for item in json_data:
            id_index = replace_ids(item, new_ids, id_index)
    return id_index


def test():
  with open("curl.txt", "r") as arquivo:
    protoCurl = arquivo.read()


  try:
      result = subprocess.check_output(protoCurl, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)

  except subprocess.CalledProcessError as cpe:
      result = cpe.output

  finally:
      for line in result.splitlines():
        print(line.decode())
      #    if '1001' in line.decode():
      #      print("ok")
      #print(result.splitlines())
      if 'Connection' in result.splitlines():
        print("ok")
      print(type(result.splitlines()))

