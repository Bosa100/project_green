#!/usr/bin/python3

'''
This program is a simple alarm system. It imports the ips array from getJson and uses
that to check the levels at each sensor. It iterates through ips, fills levels with
the sensor server responses, and then checks each level and populates warnings based on what was found.

warning codes:
     0 : safe level
    -1 : dangerously low
    -2 : dangerously high
by: Braulio Salcedo
'''

import sys
sys.path.insert(0, '/home/salcbrau/project_green/Software/Python/')
import time
from getJson import *
import json
import smtplib
from twilio.rest import Client


'''
retrieves data from sensors
    loops through ips array - get() is imported from getJson
'''
def getData():
    type = 'm'
    for i in range(len(ips)):
        if i == 1:
            type = "th"
        elif i == 2:
            type = "l"
        for j in range(len(ips[i])):
            result = get(ips[i][j], type)
            # get returns -1 if data was "nan" - if -1 skips
            # ip to avoid problems
            print(ips[i][j])
            if (result != -1):
                # data retrieved succesfuly, results gets sent to
                # check level
                levels[i][j] = result
                checkLevel(levels[i][j], type, j)

'''
checks data passed and sets warnings array at proper index
    MIN/MAX values imported from getJson()
'''
def checkLevel(data, which, j):
    # checks type of data (might send single or double data depending on sensor)
    if which == 'm':
        # no max for moisture
        if data > MIN_MOIST:
            warnings[0][j] = -1
    elif which == 'th':
        # loops through data (th returns an array with both t and h values)
        for i in range(len(data)):
            # 0 is temp data - sends both F and C
            # 1 is humididty data
            if i == 0:
                curr = data[i][1]
                if curr < MIN_TEMP:
                    warnings[1][j][i] = -1
                elif curr > MAX_TEMP:
                    warnings[1][j][i] = -2
            elif i == 1:
                curr = data[i]
                if curr < MIN_HUMI:
                    warnings[1][j][i] = -1
                elif curr > MAX_HUMI:
                    warnings[1][j][i] = -2
    elif which == 'l':
        for i in range(len(data)):
            curr = data[i]
            if i == 0:
                curr = data[i]
                if curr < MIN_LIGHT:
                    warnings[2][j][i] = -1
                elif curr > MAX_LIGHT:
                    warnings[2][j][i] = -2
            elif i == 1:
                if curr < MIN_UV:
                    warnings[2][j][i] = -1
                elif curr > MAX_UV:
                    warnings[2][j][i] = -2
'''
iterates through warnings array and creates message based on warning codes
    appends to message variable then sends at the end
'''
def createMessage():
    header = "ALERT! Dangerous conditions in Green House\n==========================================\n"
    message = ""
    for i in range(len(warnings)):
        for j in range(len(warnings[i])):
            if i == 0:
                state = warnings[i][j]
                kind = "Moisture"
                if state == -1:
                    level = "low"
                    num = j + 1
                    val = levels[i][j]
                    message += "%s level dangerously %s at sensor #%d ( %.2f ).\n" % (kind, level, num, float(val))
            else:
                for k in range(len(warnings[i][j])):
                    state = warnings[i][j][k]
                    if state != 0:
                        
                        if state == -1:
                            level = "low"
                        elif state == -2:
                            level = "high"
                            
                        if i == 1:
                            num = 6 + j
                            if k == 0:
                                kind = "Temperature"
                                val = levels[i][j][k][1]
                            elif k == 1:
                                kind = "Humidity"
                                val = levels[i][j][k]
                        elif i == 2:
                            num = 8 + j
                            if k == 0:
                                kind = "Light intensity"
                            elif k == 1:
                                kind = "UV light"
                            val = levels[i][j][k]
                        message += "%s level dangerously %s at sensor #%d ( %.2f ).\n" % (kind, level, num, float(val))
    # true if message is not "", which would mean no sensors were at danger zone
    if message:
        print(header + message)
        sendAlerts(header + message)
    else:
        print("No message created")

def sendAlerts(text):
    # sends email
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('DUGreenhouseAlerts@gmail.com', 'TeamGreen4')
    mail.sendmail('DUGreenhouseAlerts@gmail.com', 'salcbrau@my.dom.edu', text)
    mail.close()

    # sends text message
    account_sid="ACc3ef768bb932aa094df21c031c070e84" 
    auth_tokken="9bbc933b853e34e50250fdbc1e60db07" 
    client = Client(account_sid, auth_tokken)
    message = client.api.account.messages.create(to="+16307475480",from_="+17738325163",body=text)

# main method
# initializes warnings/levels array
if __name__ == '__main__':
    warnings = [[0, 0, 0, 0, 0],[[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0]]]
    levels = [[0, 0, 0, 0, 0],[[0,0],[0,0]],[[0,0],[0,0],[0,0],[0,0],[0,0]]]
    
    print(interval_alarm)
    # implements system - time.sleep() stops program for set amount of time
    # interval_alarm imported from getJson.py
    
    while(True):
        getData()
        createMessage()
        time.sleep(interval_alarm)
