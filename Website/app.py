from flask import Flask, render_template, url_for
import os
import json
import urllib.request
import sqlite3

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

def getJson(ip):
    res = urllib.request.urlopen(ip)
    data_dict = json.loads(res.read().decode('utf-8'))
    return data_dict

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def demo():
    return render_template('demo_start.html')

@app.route('/demo/moisture/<num>/<address>')
def moisture(num, address):
    '''url = "http://" + address
    data_dict = getJson(url)
    moisture = data_dict["moisture"]'''
    moisture = 5
    #c.execute("INSERT INTO moisture" + num + "(moisture)", (moisture))
    return render_template('moisture.html', data = moisture, num = num)
    


@app.route('/demo/sensor6')
def sensor6():
    data_dict = getJson("http://10.0.192.165")
    return render_template('data.html')

@app.route('/test')
def test():
    name = "Jose"
    return render_template('data.html', word = name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



