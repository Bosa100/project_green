from flask import Flask, render_template
<<<<<<< HEAD
import json
import urllib.request
import sqlite3
=======
>>>>>>> databaseDevelopment

app = Flask(__name__)

db = sqlite3.connect("/home/pi/project_green/Database/database.db")
c = db.cursor()

def getJson(ip):
    res = urllib.request.urlopen(ip)
    data_dict = json.loads(res.read().decode('utf-8'))
    return data_dict

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/demo')
def cake():
    return render_template('demo_start.html')

@app.route('/demo/moisture/<num>/<address>')
def sensor(num, address):
    url = "http://" + address
    data_dict = getJson(url)
    moisture = data_dict["moisture"]
    c.execute("INSERT INTO moisture" + num + "(moisture)", (moisture))
    return render_template('data.html', data = moisture)


@app.route('/demo/sensor6')
def sensor6():
    data_dict = getJson("http://10.0.192.165")
    return render_template('data.html')

@app.route('/test')
def test():
    name = "Jose"
    return render_template('data.html', word = name)

@app.route('/json')
def getJson():
    import json
    import urllib.request
    res = urllib.request.urlopen("http://10.0.192.17")
    data_dict = json.loads(res.read().decode('utf-8'))
    temp = data_dict["temperature"]
    return str(temp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



