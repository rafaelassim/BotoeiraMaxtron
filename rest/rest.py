import requests
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

def send_rest(package):



    send_json
    return


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
url = "https://exemplo.com/api"

# Lista com os novos valores de Id
novos_ids = [10222222222222221, 102, 103, 104]

# Atualizando o JSON com os novos valores de Id
replace_ids(mission_two_steps, novos_ids)


username = "seu_usuario"
password = "sua_senha"

#resultado = send_json(url, data, username, password)
#print(f"Resultado: {resultado}")

print(mission_two_steps)