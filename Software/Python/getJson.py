import json
from urllib.request import urlopen 
from urllib.error import URLError
import datetime
# missing one temperature and one sunlight
# 10.0.192.226 missing light
# 10.0.192.229 missing th

ips = [["10.0.192.222", "10.0.192.221", "10.0.192.218", "10.0.192.224", "10.0.192.223"],["10.0.192.225", "10.0.192.220"],["10.0.192.226", "10.0.192.228", "10.0.192.219", "10.0.192.230", "10.0.192.227"]]

def get(ip, kind):
    url = "http://" + ip
    got_data = False
    while (got_data == False):
        try:
            res = urlopen(url)
            got_data = True
        except URLError as e:
            got_data = False
            
    data_dict = json.loads(res.read().decode('utf-8'))

    #gets data
    if kind == 'th':
        data = [data_dict["temperature"][0], data_dict["humidity"][0]]        
    elif kind == 'm':
        data = data_dict["moisture"][0]
    elif kind == 'l':
        data = [data_dict["visible_light"][0], data_dict["UV_light"][0]]
    return data    

def send(num, ip, kind, db, c):
    data = get(ip, kind)
    date = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")

    if kind == 'm':
        sql = "INSERT INTO Moisture (ID, Moisture, Date) VALUES (?, ?, ?)"
        values = (num, data, date)
        c.execute(sql, values)
        db.commit()
    elif kind == 'th':
        data_f = 9.0/5.0 * data[0] + 32
        sql = "INSERT INTO Temperature (ID, Fahrenheit, Celsius, DATE) VALUES (?, ?, ?, ?)"
        values = (num, data[0], data_f, date)
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
