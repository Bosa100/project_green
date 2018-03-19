import json
import urllib.request

def get(ip, kind):
    url = "http://" + ip
    res = urllib.request.urlopen(url)
    data_dict = json.loads(res.read().decode('utf-8'))

    #gets data
    if kind == 't':
        data = data_dict["temperature"][0]        
    elif kind == 'h':
        data = data_dict["humidity"][0]
    else:
        data = data_dict["moisture"][0]

    return data    


    
