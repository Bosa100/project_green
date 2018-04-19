import json
import urllib.request

def get(ip, kind):
    url = "http://" + ip
    res = urllib.request.urlopen(url)
    data_dict = json.loads(res.read().decode('utf-8'))

    #gets data
    if kind == 'th':
        data = [data_dict["temperature"][0], data_dict["humidity"][0]        
    elif kind == 'm':
        data = data_dict["moisture"][0]
	 elif kind == 'l':
			data = [data_dict["light"][0], data_dict["uvindex"][0]]
    return data    


    
