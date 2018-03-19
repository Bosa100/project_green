import getJson
import time

    IP_MOIST1 = "10.0.192.XXX"
    IP_MOIST2 = "10.0.192.XXX"
    IP_MOIST3 = "10.0.192.XXX"
    IP_MOIST4 = "10.0.192.XXX"
    IP_MOIST5 = "10.0.192.XXX"
    IP_TEMP_HUMI = "10.0.192.XXX"

    MAX_MOIST = 75
    MAX_TEMP = 100
    MAX_HUMI = 75

    m1Danger = false
    m2Danger = false
    m3Danger = false
    m4Danger = false
    m5Danger = false

    tempDanger = false
    humiDanger = false
    
    def getMoist():
        m1 = getJson.get(IP_MOIST1, 'm')
        m2 = getJson.get(IP_MOIST1, 'm')
        m3 = getJson.get(IP_MOIST1, 'm')
        m4 = getJson.get(IP_MOIST1, 'm')
        m5 = getJson.get(IP_MOIST1, 'm')
        return [m1, m2, m3, m4, m5]

    def getTempHumi():
        t = getJson.get(IP_TEMP_HUMI, 't')
        h = getJson.get(IP_TEMP_HUMI, 'h')
        return [t, h]

    def checkLevels(mArr, thArr):
        for 

    while(true):
        m = getMoist()
        th = getTempHumi()
        checkLevels(m, thArr)
        time.sleep(1800)


