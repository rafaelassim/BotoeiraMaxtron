
import json

configjson      = 'Data/config.json'
maquinasjson    = 'Data/maquinas.json'
produtosjson    = 'Data/produtos.json'
qrcodemaqjson   = 'Data/qrcodemaq.json'
qrcodeprodjson  = 'Data/qrcodeprod.json'


def region_list():
    arqmaq = open(maquinasjson)
    data = json.load(arqmaq)
    region =[]
    for item in data.values():
        for data_item in item.keys():
            region.append(data_item)
    return (region)


def maq_region_list(region):
    arqprod = open(maquinasjson)
    data = json.load(arqprod)
    produtos =[]
    print(data["region"][region].keys())
    localjson = data["region"][region]
    for item in localjson.keys():
        produtos.append(item)
    return (produtos)

    
def tag_machines(region,maquina):
    arqmaq = open(maquinasjson)
    data = json.load(arqmaq)
    return(data["region"][region][maquina]['Tag'],data["region"][region][maquina]['Order_ID'])
   

   
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

def tagproduto(bitola, item):
    arqprod = open(produtosjson)
    data = json.load(arqprod)
    tag =data["Produtos"][bitola][item]['Tag']
    id=data["Produtos"][bitola][item]['Order_ID']
    return (tag,id)

def tagqrcodemaq(qrcode):
    arqprod = open(qrcodemaqjson)
    data = json.load(arqprod)
    try:
        tag =data["qrcodemaq"][qrcode]['Tag']
        id=data["qrcodemaq"][qrcode]['Order_ID']
        return (tag,id)
    except:

        return (None)
def nomeqrcodemaq(qrcode):
    arqprod = open(qrcodemaqjson)
    data = json.load(arqprod)
    try:
        nome =data["qrcodemaq"][qrcode]['Nome']
        return (nome)
    except:

        return (None)

def tagqrcodprod(qrcode):
    arqprod = open(qrcodeprodjson)
    data = json.load(arqprod)
    try:
        tag =data["qrcodeprod"][qrcode]['Tag']
        id =data["qrcodeprod"][qrcode]['Order_ID']
        return (tag,id)
    except:

        return (None)
def nomeqrcodprod(qrcode):
    arqprod = open(qrcodeprodjson)
    data = json.load(arqprod)
    try:
        nome =data["qrcodeprod"][qrcode]['Nome']
        return (nome)
    except:

        return (None)


def nomeqrcodprod(qrcode):
    arqprod = open(qrcodeprodjson)
    data = json.load(arqprod)
    try:
        nome =data["qrcodeprod"][qrcode]['Nome']
        return (nome)
    except:

        return (None)

def config():
    arqconfig = open(configjson)
    data = json.load(arqconfig)
    ID=1
    IP = "192.168.0.100"
    PORT = 8015
    try:
        IP   =data["IP"]
        PORT =data["PORT"]
        ID   =data["ID"]
        print("IP DO GERENCIADOR ",IP)
        print("PORTA DO GERENCIADOR ",PORT)
        return (ID,IP,PORT)
    except:
        return (ID,IP,PORT)

 
#print("Maq: ", tagqrcodprod("404004305233528516575584976473448"))

#print(region_list())
#print(maq_region_list("A"))
#print(tag_machines("A","415"))
#print("Maq: ", qrcodemaq("4115"))
#print(len(machines_list()))
#print(machines_data('439'))
#print(produto_bitola_list())
#print(produto_bitola_items('1'))
#print(tag_produto('1','1,0 BE13 ESPECIAL'))
