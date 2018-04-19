from getJson import *

db = sqlite3.connect("/home/pi/project_green/Database/GreenhouseSensors")
c = db.cursor()
for i in range(len(ips)):
	if i == 0:
		type = 'th'
	elif i == 1:
		type = 'm'
	elif i == 2:
		type == 'l'
	for j in range(len(ips[i]):
		send(ips[i][j], type) 
