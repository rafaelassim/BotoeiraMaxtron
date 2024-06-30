
import json
# Opening JSON file

maquinasjson = 'Data/maquinas.json'
produtosjson = 'Data/produtos.json'
qrcodemaqjson   = 'Data/qrcodemaq.json'
qrcodeprodjson   = 'Data/qrcodeprod.json'


def machines_list():
    arqmaq = open(maquinasjson)
    data = json.load(arqmaq)
    maquinas =[]
    for item in data.values():
        for data_item in item.keys():
            maquinas.append(data_item)
    return (maquinas)
    
def tag_machines(maquina):
    arqmaq = open(maquinasjson)
    data = json.load(arqmaq)
    return(data["Maquina"][maquina]['Tag'])
   

   
def produto_bitola_list():
    arqprod = open(produtosjson)
    data = json.load(arqprod)
    maquinas =[]
    for item in data.values():
        for data_item in item.keys():
            maquinas.append(data_item)
    return (maquinas)
    
def produto_bitola_items(bitola):
    arqprod = open(produtosjson)
    data = json.load(arqprod)
    produtos =[]
    print(data["Produtos"][bitola].keys())
    localjson = data["Produtos"][bitola]
    for item in localjson.keys():
        produtos.append(item)
    return (produtos)
def tag_produto(bitola, item):
    arqprod = open(produtosjson)
    data = json.load(arqprod)
    produto =data["Produtos"][bitola][item]['Tag']
    #print(data["Produtos"][bitola].keys())
    return (produto)

def tagqrcodemaq(qrcode):
    arqprod = open(qrcodemaqjson)
    data = json.load(arqprod)
    try:
        tag =data["qrcodemaq"][qrcode]['Tag']
        return (tag)
    except:

        return (None)
def nomeqrcodemaq(qrcode):
    arqprod = open(qrcodemaqjson)
    data = json.load(arqprod)
    try:
        tag =data["qrcodemaq"][qrcode]['Nome']
        return (tag)
    except:

        return (None)

def tagqrcodprod(qrcode):
    arqprod = open(qrcodeprodjson)
    data = json.load(arqprod)
    try:
        tag =data["qrcodeprod"][qrcode]['Tag']
        return (tag)
    except:

        return (None)
def nomeqrcodprod(qrcode):
    arqprod = open(qrcodeprodjson)
    data = json.load(arqprod)
    try:
        tag =data["qrcodeprod"][qrcode]['Nome']
        return (tag)
    except:

        return (None)

#print("Maq: ", tagqrcodprod("404004305233528516575584976473448"))


#print("Maq: ", qrcodemaq("4115"))
#print(len(machines_list()))
#print(machines_data('439'))
#print(produto_bitola_list())
#print(produto_bitola_items('1'))
#print(tag_produto('1','1,0 BE13 ESPECIAL'))
