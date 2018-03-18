from flask import Flask, render_template, url_for
import os
import json
import urllib.request
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

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

@app.route('/getJson/<ip>/<kind>')
def getJson(ip, kind):

    '''
    url = "http://" + ip
    res = urllib.request.urlopen(url)
    data_dict = json.loads(res.read().decode('utf-8'))

    #gets data
    if kind == 't':
        data = data_dict["temperature"]
    elif kind == 'h':
        data = data_dict["humidity"]
    else:
        data = data_dict["moisture"]
    '''
    return ip

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo_start.html')

@app.route('/demo/moisture/<num>/<address>')
def moisture(num, address):
    '''
    db = sqlite3.connect("/home/pi/project_green/Database/database.db")
    c = db.cursor()
    url = "http://" + address
    data_dict = getJson(url)
    moisture = data_dict["moisture"]
    moisture = 5
    c.execute("INSERT INTO moisture" + num + " (moisture) VALUES(?)", (moisture,))
    '''
    return render_template('moisture.html', ip = address, num = num)
    
@app.route('/demo/temp-humi/<address>')
def th_sensor(address):
    '''url = "http://" + address
    data_dict = getJson(url)
    moisture = data_dict["moisture"]'''
    return render_template('temp-humi.html', ip = address)

@app.route('/make_graph/<type>')
def make_graph(type):

    '''
    if type = 't':
        code for t
    elif type = 'h':
        code for h
    else
        code for m
    '''
    #db = sqlite3.connect("/home/pi/project_green/Database/database.db")
    #c = db.cursor()

    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure() and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
    title='About as simple as it gets, folks')
    ax.grid()

    url = "/static/images/graphs/graph.png"
    fig.savefig("static/images/graphs/graph.png")
    return render_template('graph.html', url = url)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



