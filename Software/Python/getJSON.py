import json
import urllib.request

db = sqlite3.connect("/home/pi/project_green/Database/GreenhouseSensors")
c = db.cursor()
  



def get(ip, kind):
    url = "http://" + ip
    res = urllib.request.urlopen(url)
    data_dict = json.loads(res.read().decode('utf-8'))

    #gets data
    if kind == 'th':
        data = [data_dict["temperature"][0], data_dict["humidity"][0]        
    elif kind == 'm':
        data = data_dict["moisture"][0]
	 elif kind == 'l':
			data = [data_dict["light"][0], data_dict["uvindex"][0]]
    return data    

get send(num, ip, kind):
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
        values = (num, data, date)
		  c.execute(sql, values)
		  db.commit()
	elif kind == 'l':
		data = data_dict["visible_light"][0]
        sql = "INSERT INTO Light (ID, Light, DATE) VALUES (?, ?, ?)"
        values = (num, data, date)
		c.execute(sql, values)
      db.commit()
      data = data_dict["UV_light"][0]
        sql = "INSERT INTO UV (ID, UVIndex, DATE) VALUES (?, ?, ?)"
        values = (num, data, date)
		c.execute(sql, values



		  
