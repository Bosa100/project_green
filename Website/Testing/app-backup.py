from flask import Flask, render_template
import json
import urllib.request
import sqlite3

app = Flask(__name__)

db = sqllite3.connect("/home/pi/project_green/Database/database.db")
c = db.cursor()

def getJson(ip):
    res = urllib.request.urlopen(ip)
    data_dict = json.loads(res.read().decode('utf-8'))
    #temp = data_dict["moisture"]
    #jsonString = res.read()
    return data_dict

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def cake():
    return render_template('demo_start.html')

@app.route('/demo/moisture1')
def sensor1():
    data_dict = getJson("http://10.0.192.146")
    
    return render_template('data.html', data = data)

@app.route('/demo/sensor2')
def sensor2():
    data_dict = getJson("http://10.0.192.163" data = data)
    moisture = data_dict["moisture"]
    c.execute('''INSERT INTO moisture1(moisture)''', (moisture)) 
    return render_template('data.html')

@app.route('/demo/sensor3')
def sensor3():
    data_dict = getJson("http://10.0.192.44" data = data)
    return render_template('data.html')

@app.route('/demo/sensor4')
def sensor4():
    data_dict = getJson("http://10.0.192.159" data = data)
    return render_template('data.html')

@app.route('/demo/sensor5')
def sensor5():
    data_dict = getJson("http://10.0.192.54" data = data)
    return render_template('data.html')

@app.route('/demo/sensor6')
def sensor6():
    data_dict = getJson("http://10.0.192.165" data = data)
    return render_template('data.html')

@app.route('/test')
def test():
    name = "Jose"
    return render_template('data.html', name = name)

@app.route(

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



