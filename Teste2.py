
import json
json_data = []
with open('maquinas.json') as json_file:
    json_data = json.load(json_file)
for key, value in json_data.iteritems():
    print (key) 
    for item in value: 
        print (item)
        for key, value in json_data.iteritems(): 
            print (key)
            for item in value: 
                print (item)