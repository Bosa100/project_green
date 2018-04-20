from getJson import *
import sqlite3
import time

db = sqlite3.connect("/home/pi/project_green/Database/GreenhouseSensors")
c = db.cursor()

while(True):
        for i in range(len(ips)):
                if i == 0:
                        type = 'm'
                elif i == 1:
                        type = 'th'
                elif i == 2:
                        type = 'l'
                for j in range(len(ips[i])):
                        print(ips[i][j])
                        print(i)
                        print(j)
                        send(j + 1, ips[i][j], type, db, c)
        time.sleep(900)


