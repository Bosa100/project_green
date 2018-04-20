import json
import urllib.request
import time

ips = [["10.0.192.222", "10.0.192.221", "10.0.192.218", "10.0.192.224", "10.0.192.223"],["10.0.192.XXX", "10.0.192.XXX", "10.0.192.220"],["10.0.192.XXX", "10.0.192.XXX", "10.0.192.219", "10.0.192.XXX". "10.0.192.XXX"]]
danger_flags = [[false, false, false, false, false],[false, false, false],[false, false, false, false, false]]
levels = [[0, 0, 0, 0, 0],[0,0,0],[0, 0, 0, 0, 0]]

MAX_MOIST = 75
MAX_TEMP = 100
MAX_HUMI = 75

    
def getData():
    type = 'm'
    for i in range(len(ips)):
        if i == 1:
            type = "th"
        elif i == 2:
            type = "l"
        for j in range(len(ips[i])):
            levels[i][j] = get(ips[i][j], type)
            
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

    check_level(data, kind)
    return data    

def check_level(level, which):
    if which 
    
    


