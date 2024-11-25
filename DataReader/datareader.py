
import json

configjson      = '/home/tunkers/BotoeiraMaxtron/Data/config.json'
maquinasjson    = '/home/tunkers/BotoeiraMaxtron/Data/maquinas.json'
produtosjson    = '/home/tunkers/BotoeiraMaxtron/Data/produtos.json'
qrcodemaqjson   = '/home/tunkers/BotoeiraMaxtron/Data/qrcodemaq.json'
qrcodeprodjson  = '/home/tunkers/BotoeiraMaxtron/Data/qrcodeprod.json'
filasjson  = '/home/tunkers/BotoeiraMaxtron/Data/qrcode_fila.json'

#configjson      = 'Data/config.json'
#maquinasjson    = 'Data/maquinas.json'
#produtosjson    = 'Data/produtos.json'
#qrcodemaqjson   = 'Data/qrcodemaq.json'
#qrcodeprodjson  = 'Data/qrcodeprod.json'

def return_maquinas(region):
    arqmaq = open(maquinasjson)
    data = json.load(arqmaq)
    
    return data["region"][region]


def region_list():
    arqmaq = open(maquinasjson)
    data = json.load(arqmaq)
    region =[]
    #print (data["region"]["COM"]["strech"])
    #print(len(data["region"]["COM"]["strech"]))
    for item in data.values():
        for data_item in item.keys():
            region.append(data_item)
    return (region)

def nomeqrcodemaq(region):
    arqmaq = open(qrcodemaqjson)
    data = json.load(arqmaq)
    return data["region"][region]



def return_product():
    arqproduto = open(produtosjson)
    data = json.load(arqproduto)
    
    return data["Produtos"]
    
def maq_region_list(region):
    arqprod = open(maquinasjson)
    data = json.load(arqprod)
    produtos =[]
    #print(data["region"][region].keys())
    localjson = data["region"][region]
    for item in localjson.keys():
        produtos.append(item)
    return (produtos)


def maq_missions_list(region,maq):
    arqmaq = open(maquinasjson)
    data = json.load(arqmaq)
    produtos =[]
    #print(data["region"][region].keys())
    localjson = data["region"][region][maq]
    for item in localjson.keys():
        produtos.append(item)
    return (produtos)


def tag_machines(region,maquina,mission):
    arqmaq = open(maquinasjson)
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


def return_qrproduct():
    arqproduto = open(qrcodeprodjson)
    data = json.load(arqproduto)
    
    return data["Produtos"]

def return_qrfilas():
    arqproduto = open(filasjson)
    data = json.load(arqproduto)
    
    return data["Filas"]
    
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

#print(return_qrproduct()["40472728"])
#print(return_product()["1"] ["BE13 ESPECIAL "]["SKU"])
#print(nomeqrcodemaq()["region"]["COM"]["21"])
#maq = return_maquinas("COM")
#print(len(return_maquinas("COM")))
#print(list(maq.keys())[5])
#print("dddd", list(maq.keys()))
#print(len(maq["11"]))
#print(maq.keys())
#print(list(maq["11"]["material_type"].split(',')))
#print(len(maq["11"]["material_type"].split(',')))
#print(tag_machines("A","Maquina A","DESCARTE"))