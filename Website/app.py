from flask import Flask, render_template, url_for
import os
import json
import urllib.request
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pymysql
import datetime

app = Flask(__name__)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/getJson/<ip>/<kind>/<num>')
def getJson(ip, kind, num):
    url = "http://" + ip
    res = urllib.request.urlopen(url)
    data_dict = json.loads(res.read().decode('utf-8'))
    date = datetime.datetime.now().strftime("%I:%M:%s%p on %B %d, %Y")
    #gets data
    if kind == 't':
        data = data_dict["temperature"][0]
        data_f = 9.0/5.0 * data + 32
        sql = "INSERT INTO Temperature (ID, Fahrenheit, Celsius, DATE) VALUES (?, ?, ?, ?)"
        values = (num, data_f, data, date)
    elif kind == 'h':
        data = data_dict["humidity"][0]
        sql = "INSERT INTO Humidity (ID, Humidity, DATE) VALUES (?, ?, ?)"
        values = (num, data, date)
    elif kind == 'm':
        data = data_dict["moisture"][0]
        sql = "INSERT INTO Moisture (ID, Moisture, Date) VALUES (?, ?, ?)"
        values = (num, data, date)
    elif kind == 'n':
        data = data_dict["visible_light"][0]
        sql = "INSERT INTO Light (ID, Light, DATE) VALUES (?, ?, ?)"
        values = (num, data, date)
    else:
        data = data_dict["UV_light"][0]
        sql = "INSERT INTO UV (ID, UVIndex, DATE) VALUES (?, ?, ?)"
        values = (num, data, date)

    db = sqlite3.connect("/home/pi/project_green/Database/GreenhouseSensors")
    c = db.cursor()
    c.execute(sql, values)
    db.commit()
    c.close()
    db.close()
    return str(data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo_start.html')

@app.route('/demo/moisture/<num>/<address>')
def moisture(num, address):
    return render_template('moisture.html', ip = address, num = num)
    
@app.route('/demo/temp-humi/<address>/<num>')
def th_sensor(address, num):
    '''url = "http://" + address
    data_dict = getJson(url)
    moisture = data_dict["moisture"]'''
    return render_template('th_sensor.html', ip = address, num = num)

@app.route('/demo/light/<address>/<num>')
def light(num, address):
    return render_template('light_sensor.html', ip = address, num = num)

def populate_ids(ids, start, end):
    num = start
    range_end = end - start + 1
    for ndx in range(0, range_end):
        np.append(ids, num)
        print(num)
        num += 1
   
@app.route('/make_graph/<which>/<start>/<end>')
def make_graph(which, start, end):
    #db = MySQLdb.connect(host="localhost", user="john", passwd="megajonhy", db="jonhydb") 
    #cur = db.cursor()
    if which == 't':
        name = "Temperature Data"
        ylabel = "Temperature"
        sql = "SELECT Celsius FROM Temperature WHERE rowid BETWEEN " + start + " AND " + end
    elif which == 'h':
        name = "Humidity Data"
        ylabel = "Humidity"
        sql = "SELECT Humidity FROM Humidity WHERE rowid BETWEEN " + start + " AND " + end 
    elif which == 'm':
        name = "Moisture Data"
        ylabel = "Moisture"
        sql = "SELECT Moisture FROM Moisture WHERE rowid BETWEEN " + start + " AND " + end
    elif which == 'n':
        name = "Light Intensity Data"
        ylabel = "Light Intensity"
        sql = "SELECT Light FROM Light WHERE rowid BETWEEN " + start + " AND " + end
    else:
        name = "UV Index"
        ylabel = "UV Index"
        sql = "SELECT UVIndex FROM UV WHERE rowid BETWEEN " + start + " AND " + end


    db = sqlite3.connect("/home/pi/project_green/Database/GreenhouseSensors")
    c = db.cursor()
    
    c.execute(sql)
    rows = c.fetchall()
    
    c.close()
    db.close()
    
    # Data for plotting
    ids = np.arange(int(start), int(end) + 1)
    data = np.array(rows)

    #populate_ids(ids, int(start), int(end))
    #populate_data(ids, data)

    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure() and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    ax.xaxis.set_ticks(np.arange(min(ids), max(ids) + 1, 1.0))
    ax.plot(ids, data)

    ax.set(xlabel='ID', ylabel=ylabel, title=name)
    ax.grid()

    url = "images/graphs/graph.png"
    fig.savefig("static/" + url)

    return render_template('graph.html', url = url)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
