#!/usr/bin/python3
import sys
sys.path.insert(0, "/home/salcbrau/project_green/Software/Python")

from getJson import *
import sqlite3
import time

if __name__ == '__main__':
        # connects to database
        db = sqlite3.connect("/home/salcbrau/project_green/Database/GreenhouseSensors")
        c = db.cursor()
        
        print(interval_data)
        # infinite loop that gets called every X minutes (interval_data - from getJson.py
        while(True):
                # loops through ips array and calls send function (getJson.py) to
                # send data into database
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
                                print(ips[i][j])
                time.sleep(interval_data)

        



