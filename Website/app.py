from flask import Flask, render_template, url_for
import os
import json
import urllib.request
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import pymysql

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
def getJson(ip, kind):

    url = "http://" + ip
    res = urllib.request.urlopen(url)
    data_dict = json.loads(res.read().decode('utf-8'))

    #gets data
    if kind == 't':
        data = data_dict["temperature"][0]
        
    elif kind == 'h':
        data = data_dict["humidity"][0]
    else:
        data = data_dict["moisture"][0]

    db = sqlite3.connect("/home/pi/project_green/Database/database.db")
    c = db.cursor()
    url = "http://" + address
    data_dict = getJson(url)
    moisture = data_dict["moisture"]
    moisture = 5
    c.execute("INSERT INTO moisture" + num + " (moisture) VALUES(?)", (moisture,))
    
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
    
@app.route('/demo/temp-humi/<address>')
def th_sensor(address):
    '''url = "http://" + address
    data_dict = getJson(url)
    moisture = data_dict["moisture"]'''
    return render_template('temp-humi.html', ip = address)

def populate_ids(ids, start, end):
    num = start
    range_end = end - start + 1
    for ndx in range(0, range_end):
        np.append(ids, num)
        print(num)
        num += 1

def populate_data(ids, data):
    data = [1, 2, 3, 4, 5]
        
@app.route('/make_graph/<which>/<start>/<end>')
def make_graph(which, start, end):
    #db = MySQLdb.connect(host="localhost", user="john", passwd="megajonhy", db="jonhydb") 
    #cur = db.cursor()
    
    if which == 't':
        name = "Temperature Data"
        ylabel = "Temperature"
    elif which == 'h':
        name = "Humidity Data"
        ylabel = "Humidity"
    else:
        name = "Moisture Data"
        ylabel = "Moisture"
        
    # Data for plotting
    ids = np.array([1, 2, 3, 4, 5])
    data = np.array([1, 2, 3, 4, 5])

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
