
import json

configjson      = '/home/tunkers/BotoeiraMaxtron/Data/config.json'
maquinasjson    = '/home/tunkers/BotoeiraMaxtron/Data/maquinas.json'
produtosjson    = '/home/tunkers/BotoeiraMaxtron/Data/produtos.json'
qrcodemaqjson   = '/home/tunkers/BotoeiraMaxtron/Data/qrcodemaq.json'
qrcodeprodjson  = '/home/tunkers/BotoeiraMaxtron/Data/qrcodeprod.json'


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


def maq_missions_list(region,maq):
    arqmaq = open(maquinasjson)
    #arqprod = open("/home/rafael/Documentos/Projetos/Python/BotoeiraMaxtron/Data/maquinas.json")
    data = json.load(arqmaq)
    produtos =[]
    print(data["region"][region].keys())
    localjson = data["region"][region][maq]
    for item in localjson.keys():
        produtos.append(item)
    return (produtos)


def tag_machines(region,maquina,mission):
    arqmaq = open(maquinasjson)
    #arqmaq = open("/home/rafael/Documentos/Projetos/Python/BotoeiraMaxtron/Data/maquinas.json")
    data = json.load(arqmaq)

    try:
        #tag =data["region"][region][maquina]['Tag']
        #id=data["region"][region][maquina]['Order_ID']
        #descarte=data["region"][region][maquina]['TagDescarte']
        #lgv=data["region"][region][maquina]['LGV']
        return(data["region"][region][maquina][mission])
        #return (tag,id,descarte,lgv)

    except:
        print("Maquinas não encontradas")
    return(None)
   

   
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
    #tag =data["Produtos"][bitola][item]['Tag']
    #id=data["Produtos"][bitola][item]['Order_ID']
    return (data["Produtos"][bitola][item])

def tagqrcodemaq(qrcode):
    arqprod = open(qrcodemaqjson)
    data = json.load(arqprod)
    
    try:
        #tag =data["qrcodemaq"][str(qrcode)]['Tag']
        #id=data["qrcodemaq"][str(qrcode)]['Order_ID']
        #descarte=data["qrcodemaq"][str(qrcode)]['TagDescarte']
        #lgv=data["qrcodemaq"][str(qrcode)]['lgv']
        return (data["qrcodemaq"][str(qrcode)])
    except:

        return (None)
def nomeqrcodemaq(qrcode):
    arqprod = open(qrcodemaqjson)
    data = json.load(arqprod)
    try:
        nome =data["qrcodemaq"][str(qrcode)]['Nome']
        return (nome)
    except:

        return (None)

def tagqrcodprod(qrcode):
    arqprod = open(qrcodeprodjson)
    data = json.load(arqprod)
    try:
        #tag =data["qrcodeprod"][qrcode]['Tag']
        #id =data["qrcodeprod"][qrcode]['Order_ID']
        return (data["qrcodeprod"][qrcode])
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


#def nomeqrcodprod(qrcode):
#    arqprod = open(qrcodeprodjson)
#    data = json.load(arqprod)
#    try:
#        nome =data["qrcodeprod"][qrcode]['Nome']
#        return (nome)
#    except:

#        return (None)

def config():
    arqconfig = open(configjson)
    data = json.load(arqconfig)
    ID=1
    IP = "192.168.0.100"
    PORT = 8015
    REGIAO ="A"
    try:
     #   IP   =data["IP-FLEETMANAGER"]
     #   PORT =data["PORT"]
     #   ID   =data["ID"]
     #   REGIAO   =data["REGIAO"]
     #   print("IP DO GERENCIADOR ",IP)
     #   print("PORTA DO GERENCIADOR ",PORT)
        return (data)
    except:
        return (ID,IP,PORT,REGIAO)


#print(maq_region_missions_list("A","Maquina A"))
#print(tag_machines("A","Maquina A","DESCARTE"))