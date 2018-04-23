import json
from urllib.request import urlopen 
from urllib.error import URLError
import datetime
# missing one temperature and one sunlight
# 10.0.192.229 missing th

# requests data from sensor servers and retrieves data
def get(ip, kind):
    url = "http://" + ip
    got_data = False
    count = 0;
    # sometimes server take a couple of tries to work, will loop until
    # data is retrieved, or until it has made 10 calls to server, at which
    # point it will return -1
    while (got_data == False):
        try:
            res = urlopen(url)
            got_data = True
        except URLError as e:
            got_data = False
            count += 1
            if (count == 10):
                return -1

    # if data waws able to be retrieved, it creates dictionary out of
    # response
    data_dict = json.loads(res.read().decode('utf-8'))

    '''
    retrieves specific data from data_dict
       - th (returns list with tempC and tempF and humidity data in second index
       - m (returns single moisture value)
       - l (returns list with visible light in first index and UV_light in second index)
    '''
    if kind == 'th':
        temp_C = data_dict["temperature"][0]
        temp_F = 9.0/5.0 * temp_C + 32
        data = [[temp_C, temp_F], data_dict["humidity"][0]]        
    elif kind == 'm':
        data = data_dict["moisture"][0]
    elif kind == 'l':
        data = [data_dict["visible_light"][0], data_dict["UV_light"][0]]
    return data    
'''
sends data to database
    num - sensor id
    db - database connection
    c - cursor
'''
def send(num, ip, kind, db, c):
    # gets current data from server
    data = get(ip, kind)
    # gets todays date and time as string
    date = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")

    # inserts into database based on type of data
    if kind == 'm':
        sql = "INSERT INTO Moisture (ID, Moisture, Date) VALUES (?, ?, ?)"
        values = (num, data, date)
        c.execute(sql, values)
        db.commit()
    elif kind == 'th':
        sql = "INSERT INTO Temperature (ID, Fahrenheit, Celsius, DATE) VALUES (?, ?, ?, ?)"
        values = (num, data[0][1], data[0][0], date)
        c.execute(sql, values)
        db.commit()
        sql = "INSERT INTO Humidity (ID, Humidity, DATE) VALUES (?, ?, ?)"
        values = (num, data[1], date)
        c.execute(sql, values)
        db.commit()
    elif kind == 'l':
        sql = "INSERT INTO Light (ID, Light, DATE) VALUES (?, ?, ?)"
        values = (num, data[0], date)
        c.execute(sql, values)
        db.commit()
        sql = "INSERT INTO UV (ID, UVIndex, DATE) VALUES (?, ?, ?)"
        values = (num, data[1], date)
        c.execute(sql, values)
        db.commit()

# creates ids array (used in alarm system and data collection system) and
# retrieves settings from Settings.json (what allows the settings to be changed)
ips = [["10.0.192.222", "10.0.192.221", "10.0.192.218", "10.0.192.224", "10.0.192.223"],["10.0.192.225", "10.0.192.220"],["10.0.192.226", "10.0.192.228", "10.0.192.219", "10.0.192.227", "10.0.192.230"]]
Settings = json.load(open("/home/pi/project_green/Software/Python/Settings.json"))
MIN_MOIST = float(Settings["min_moist"])
MIN_TEMP = float(Settings["min_temp"])
MIN_HUMI = float(Settings["min_humi"])
MIN_LIGHT = float(Settings["min_light"])
MIN_UV = float(Settings["min_UV"])
MAX_TEMP = float(Settings["max_temp"])
MAX_HUMI = float(Settings["max_humi"])
MAX_LIGHT = float(Settings["max_light"])
MAX_UV = float(Settings["max_UV"])
interval_alarm = float(Settings["alarm_system"] * 60)
interval_data = float(Settings["data_collection"] * 60)
