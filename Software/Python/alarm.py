import time
from getJson import *

def getData(ips, levels, warnings):
    type = 'm'
    for i in range(len(ips)):
        if i == 1:
            type = "th"
        elif i == 2:
            type = "l"
        for j in range(len(ips[i])):
            levels[i][j] = get(ips[i][j], type)
            checkLevel(ips, levels, warnings, data, kind, j)

def checkLevel(ips, levels, warnings, level, which, j):
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

def createMessage(warnings, levels):
    message = ""
    prompt = "%s level dangerously %s at sensor #%d ( %d ).\n"
    for i in range(len(warnings)):
        for j in range(len(warnings[i]):
            state = warnings[i][j]
            if i == 0:
                kind = "Moisture"
                if state == -1:
                    level = "low"
                    num = i + 1
                    val = levels[i][j]
            elif i == 1:
                for k in range(len(warnings[i][k]):
                    if state != 0:
                        if k == 0:
                            kind = "Temperature"
                        elif k == 1:
                            kind = "Humidity"
                            num = i + 1
                            val = levels[i][j][k]
                    if state == -1:
                        level = "low"
                    elif state == -2:
                        level = "high"
            elif i == 2:
                # code for light message
            if message != "":
                message += prompt % (kind, level, num, val)
    if message != "":
        sendAlerts(message)

def sendAlerts(message):
    
                        
                       
def main():
    ips = [["10.0.192.222", "10.0.192.221", "10.0.192.218", "10.0.192.224", "10.0.192.223"],["10.0.192.XXX", "10.0.192.XXX", "10.0.192.220"],["10.0.192.XXX", "10.0.192.XXX", "10.0.192.219", "10.0.192.XXX". "10.0.192.XXX"]]
    warnings = [[0, 0, 0, 0, 0],[0,0,0],[0,0,0,0,0]]
    levels = [[0, 0, 0, 0, 0],[0,0,0],[0, 0, 0, 0, 0]]

    MIN_MOIST = 50
    MIN_TEMP = 40
    MIN_HUMI = 20
    MAX_TEMP = 95
    MAX_HUMI = 90

    getData(ips, levels, warnings)
    createMessage(warnings, levels)
