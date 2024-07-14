import json

# JSON de exemplo
json_data = '''

    {
      "qrcodemaq": {
        "404004305233528516575584976473448":{
         "Tag":"404004305233528516575584976473448"
        },
        "415": {
          "Tag": "415"
        },
        "416": {
          "Tag": "416"
        },
        "419": {
          "Tag": "419"
        },
        "420": {
          "Tag": "420"
        },
        "421": {
          "Tag": "529"
        },
        "422": {
          "Tag": "422"
        },
        "438": {
          "Tag": "438"
        },
        "439": {
          "Tag": "439"
        },
        "443": {
          "Tag": "443"
        },
        "489": {
          "Tag": "489"
        },
        "527": {
          "Tag": "527"
        },
        "528": {
          "Tag": "528"
        },
        "670": {
          "Tag": "670"
        },
        "2015": {
          "Tag": "2015"
        },
        "6023": {
          "Tag": "6023"
        },
        "6066": {
          "Tag": "6066"
        },
        "6144": {
          "Tag": "6144"
        },
        "6146": {
          "Tag": "6146"
        },
        "6148": {
          "Tag": "6148"
        },
        "6150": {
          "Tag": "6150"
        },
        "6151": {
          "Tag": "6151"
        },
        "6155": {
          "Tag": "6155"
        },
        "6157": {
          "Tag": "6157"
        },
        "6158": {
          "Tag": "6158"
        },
        "6159": {
          "Tag": "6159"
        },
        "6161": {
          "Tag": "6161"
        },
        "6162": {
          "Tag": "6162"
        },
        "6164": {
          "Tag": "6164"
        },
        "6168": {
          "Tag": "6168"
        },
        "6169": {
          "Tag": "6169"
        },
        "6170": {
          "Tag": "6170"
        },
        "6171": {
          "Tag": "6171"
        },
        "2017": {
          "Tag": "2017"
        },
        "Depósito": {
          "Tag": "Depósito"
        },
        "Buffer Carretéis": {
          "Tag": "Buffer Carretéis"
        },
        "Buffer Palletss": {
          "Tag": "Buffer Palletss"
        },
        "Stretch": {
          "Tag": "Stretch"
        },
        "1787": {
          "Tag": "1787"
        },
        "6040": {
          "Tag": "6040"
        }
      }
    }
'''

# Converter a string JSON para um dicionário
data = json.loads(json_data)

# Inicializar o próximo Order_ID disponível
next_order_id = 1

# Função para percorrer o JSON e adicionar Order_ID onde necessário
def add_order_id(produtos):
    global next_order_id
    for category, items in produtos.items():
    #for item_name, item_data in items.items():
        if "Order_ID" not in items:
            items["Order_ID"] = next_order_id
            items["Nome"] = items["Tag"]
            next_order_id += 1

# Adicionar Order_ID aos produtos
add_order_id(data["qrcodemaq"])

# Converter o dicionário de volta para uma string JSON
updated_json_data = json.dumps(data, indent=4)

# Exibir o JSON atualizado
print(updated_json_data)