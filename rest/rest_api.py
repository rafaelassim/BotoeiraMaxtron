import requests
import os
import subprocess,sys

from requests.auth import HTTPBasicAuth

mission_two_steps={
  "ExternalId": "mm-154",
  "Name": "Manual mission 14:29:12",
  "MissionType": "Mission",
  "Options": {
    "AllowedMachines": [],
    "Priority": 4,
    "IgnoreAllowedDestinations": False,
    "AllowedAsSecondaryMission": False,
    "SecondaryMissionAllowed": False
  },
  "Steps": [
    {
      "StepType": "Pickup",
      "Options": {
        "Load": {
          "RequiredLoadStatus": "None",
          "RequiredBarcode": "",
          "LoadHeight": 0,
          "StableLoad": True
        },
        "ReservationHandling": "None",
        "MultiReservationRule": "NotAllowed",
        "SortingRules": [
          "Closest"
        ],
        "WaitSortingRules": [
          "ClosestToTarget"
        ],
        "WaitForExtension": False,
        "RequireExternalRelease": False,
        "MinimumExecutionTime": "00:00:00",
        "TargetBufferStackHeight": 0,
        "TargetBufferResourcesInStack": 1,
        "AllowStacking": True,
        "PivotDirection": "ShortestAngle"
      },
      "AllowedTargets": [
        {
          "Id": 'TARGETPICKUP1'
        }
      ],
      "AllowedWaits": []
    },
    {
      "StepType": "Dropoff",
      "Options": {
        "Load": {
          "RequiredLoadStatus": "None",
          "RequiredBarcode": "",
          "LoadHeight": 0,
          "StableLoad": True
        },
        "ReservationHandling": "None",
        "MultiReservationRule": "NotAllowed",
        "SortingRules": [
          "Closest"
        ],
        "WaitSortingRules": [
          "ClosestToTarget"
        ],
        "WaitForExtension": False,
        "RequireExternalRelease": False,
        "MinimumExecutionTime": "00:00:00",
        "TargetBufferStackHeight": 0,
        "TargetBufferResourcesInStack": 1,
        "AllowStacking": True,
        "PivotDirection": "ShortestAngle"
      },
      "AllowedTargets": [
        {
          "Id": 'TARGETDROPOFF1'
        }
      ],
      "AllowedWaits": []
    },
    {
      "StepType": "Pickup",
      "Options": {
        "Load": {
          "RequiredLoadStatus": "None",
          "RequiredBarcode": "",
          "LoadHeight": 0,
          "StableLoad": True
        },
        "ReservationHandling": "None",
        "MultiReservationRule": "NotAllowed",
        "SortingRules": [
          "Closest"
        ],
        "WaitSortingRules": [
          "ClosestToTarget"
        ],
        "WaitForExtension": False,
        "RequireExternalRelease": False,
        "MinimumExecutionTime": "00:00:00",
        "TargetBufferStackHeight": 0,
        "TargetBufferResourcesInStack": 1,
        "AllowStacking": True,
        "PivotDirection": "ShortestAngle"
      },
      "AllowedTargets": [
        {
          "Id": 'TARGETPICKUP2'
        }
      ],
      "AllowedWaits": []
    },
    {
      "StepType": "Dropoff",
      "Options": {
        "Load": {
          "RequiredLoadStatus": "None",
          "RequiredBarcode": "",
          "LoadHeight": 0,
          "StableLoad": True
        },
        "ReservationHandling": "None",
        "MultiReservationRule": "NotAllowed",
        "SortingRules": [
          "Closest"
        ],
        "WaitSortingRules": [
          "ClosestToTarget"
        ],
        "WaitForExtension": False,
        "RequireExternalRelease": False,
        "MinimumExecutionTime": "00:00:00",
        "TargetBufferStackHeight": 0,
        "TargetBufferResourcesInStack": 1,
        "AllowStacking": True,
        "PivotDirection": "ShortestAngle"
      },
      "AllowedTargets": [
        {
          "Id": 'TARGETDROPOFF2'
        }
      ],
      "AllowedWaits": []
    }
  ]
}
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
  
  
        # Enviando o JSON para a URL usando o método POST com autenticação básica
    #Abrindo o arquivo template
  with open("rest/curl.txt", "r") as arquivo:
	  template = arquivo.read()    
        # Verificando se a resposta foi recebida corretamente (status code 2xx)

 
  template=template.replace("@ID1",str(Order_ID1))
  template=template.replace("@ID2",str(Order_ID2))
  template=template.replace("@Dropoff2",str(DropOff2))
  template=template.replace("@Pickup2",str(PickUp2))
  template=template.replace("@Dropoff1",str(DropOff1))
  template=template.replace("@Pickup1",str(PickUp1))
  print("Enviando via script")
  try:
    result = subprocess.check_output(template, shell = True, executable = "/bin/bash", stderr = subprocess.STDOUT)

  except subprocess.CalledProcessError as cpe:
    result = cpe.output

  finally:  
    for line in result.splitlines():
      print(line.decode())
      if 'Connection timed' in line.decode():
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

# Exemplo de uso da função
#url = "https://exemplo.com/api"
#print(curl)
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

