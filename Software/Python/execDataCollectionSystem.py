#!/usr/bin/python3
import sys
sys.path.insert(0, "/home/pi/project_green/Software/Python")
from getJson import *
import sqlite3
import time

db = sqlite3.connect("/home/pi/project_green/Database/GreenhouseSensors")
c = db.cursor()

print(interval_data)

while(True):
        for i in range(len(ips)):
                if i == 0:
                        type = 'm'
                        id = 1
                elif i == 1:
                        type = 'th'
                        id = 6
                elif i == 2:
                        type = 'l'
                        id = 8
                for j in range(len(ips[i])):
                        
                        send(id + j, ips[i][j], type, db, c)
        time.sleep(interval_data)



