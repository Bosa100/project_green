import time

ips = [["10.0.192.222", "10.0.192.221", "10.0.192.218", "10.0.192.224", "10.0.192.223"],["10.0.192.XXX", "10.0.192.XXX", "10.0.192.220"],["10.0.192.XXX", "10.0.192.XXX", "10.0.192.219", "10.0.192.XXX". "10.0.192.XXX"]]
warnings =  [[0, 0, 0, 0, 0],[0,0,0],[0,0,0,0,0]]
levels = [[0, 0, 0, 0, 0],[0,0,0],[0, 0, 0, 0, 0]]

MIN_MOIST = 50
MIN_TEMP = 40
MIN_HUMI = 20
MAX_TEMP = 95
MAX_HUMI = 90

def getData():
    type = 'm'
    for i in range(len(ips)):
        if i == 1:
            type = "th"
        elif i == 2:
            type = "l"
        for j in range(len(ips[i])):
            levels[i][j] = get(ips[i][j], type)
				checkLevel(data, kind, j)

def get(ip, kind):
    url = "http://" + ip
    res = urllib.request.urlopen(url)
    data_dict = json.loads(res.read().decode('utf-8'))

    #gets data
    if kind == 'th':
        data = [data_dict["temperature"][0], data_dict["humidity"][0]]
    elif kind == 'm':
        data = data_dict["moisture"][0]
    elif kind == 'l':
        data = [data_dict["visible_light"][0], data_dict["UV_light"][0]]
    
	return data

def checkLevel(level, which, j):
   if which == 'm':
		if level < 50:
			warnings[0][j] = -1
   elif which == 'th':
		for i in range(levels[1])):
			if level < 40:
				warnings[1][j] = -1
 			elif level > 95:
				warnings[1][j] = -2
   elif which == 'l':
			# code to check for light levels

def sendAlerts():
	message = "%s level dangerously %s at sensor #%d ( %d )."
	for i in range(len(warnings)):
		for j in range(len(warnings[i]):
			if i == 0:
				type = "moisture"
				state = warnings[i][j]
			elif i == 1:
				
			elif state == -2:
				message += "M
				 		
					
	
