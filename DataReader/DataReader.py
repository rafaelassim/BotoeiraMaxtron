
import json
# Opening JSON file

maquinasjson = 'Data/maquinas.json'
produtosjson = 'Data/produtos.json'
def machines_list():
    arqmaq = open(maquinasjson)
    data = json.load(arqmaq)
    maquinas =[]
    for item in data.values():
        for data_item in item.keys():
            maquinas.append(data_item)
    return (maquinas)
    
def machines_data(maquina):
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
#print(len(machines_list()))
#print(machines_data('439'))
#print(produto_bitola_list())
#print(produto_bitola_items('1'))
#print(tag_produto('1','1,0 BE13 ESPECIAL'))
