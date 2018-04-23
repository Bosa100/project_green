from flask import Flask, render_template, url_for
import os
import signal
import json
import urllib.request
import sqlite3
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import numpy as np
import pymysql
import datetime
import sys
from subprocess import check_output, Popen

app = Flask(__name__)

'''
borrowed code - deals with browser cache issue (does not update css file)
source = http://flask.pocoo.org/snippets/40/
works by overriding Flask's url_for function, if used on static source it
generates url with time-stamp appended to it (guarantees CSS update)
'''
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
def getData(ip, kind, num):
    '''
    getJson route

    ip - sensor server address
    kind - type of sensor
       t -> temperature
       h -> humidity
       m -> moisture
       n -> normal light
       u -> uv light
    '''

    got_data = False
    # makes call to server and puts response into dictionary
    url = "http://" + ip
    while got_data == False:
        res = urllib.request.urlopen(url)
        data_dict = json.loads(res.read().decode('utf-8'))
        for key in data_dict:
            if data_dict[key] != "nan":
                got_data = True
            
    # current date-time
    date = datetime.datetime.now().strftime("%m-%d-%y %H:%M:%S")
    
    # uses kind arg to retrieve data from dictionary - creates sql insert query string
    # as well as list used to send arguments for query


    if kind == 'th':
        temp_C = data_dict["temperature"][0]
        temp_F = 9.0/5.0 * temp_C + 32 
        data = str(temp_C) + " " + str(temp_F) + " " + str(data_dict["humidity"][0])
    elif kind == 'l':
        data = str(data_dict["visible_light"][0]) + " " + str(data_dict["UV_light"][0])
    elif kind == 'm':
        data = data_dict["moisture"][0]
    else:
        data = ""

    return str(data)

# intro page
@app.route('/')
def index():
    today = datetime.datetime.now().strftime("%Y-%m-%dT")
    return render_template('index.html', today = today)

# demo start page
@app.route('/demo/<date>')
def demo(date):
    return render_template('demo_start.html', date = date)

def get_pid(name):
    return str(check_output(["pgrep","-f",name]))

@app.route('/modify_settings/<new_json>')
def modify(new_json):
    new_settings = json.loads(new_json)
    with open("/home/pi/project_green/Software/Python/Settings.json", "w") as jsonFile:
        json.dump(new_settings, jsonFile)
        pid_data = get_pid("dataCollectionS")
        pid_data = pid_data.replace("b'", '')
        pid_data = pid_data.split("\\n")
        pid_alarm = get_pid("alarmSystem.py")
        pid_alarm = pid_alarm.replace("b'", '')
        pid_alarm = pid_alarm.split("\\n")
        pids = [pid_data, pid_alarm]
        for i in range(len(pids)):
            for j in range(len(pids[i])):
                if(j < len(pids[i]) - 1):
                    pid = int(pids[i][j])
                    os.kill(pid, signal.SIGKILL)
        
    Popen("/home/pi/project_green/Software/Python/alarmSystem.py", shell=True)
    Popen("/home/pi/project_green/Software/Python/dataCollectionSystem.py", shell=True)
        
    return "0"

@app.route('/configure')
def config():
    settings = json.load(open("/home/pi/project_green/Software/Python/Settings.json"))
    str_settings = json.dumps(settings)
    return render_template('config_page.html', settings = str_settings)

'''
   moisture sensor page
    recieves id and ip address as parameters, which are sent to html template
'''
@app.route('/demo/moisture/<num>/<address>/<date>')
def moisture(num, address, date):
    return render_template('moisture.html', ip = address, num = num, date = date)

'''
    temp/humi page
    recieves id and ip address as parameters, which are sent to html template
''' 
@app.route('/demo/temp-humi/<address>/<num>/<date>')
def th_sensor(address, num, date):
    return render_template('th_sensor.html', ip = address, num = num, date = date)

'''
    light page
    recieves id and ip address as parameters, which are sent to html template
''' 
@app.route('/demo/light/<address>/<num>/<date>')
def light(num, address, date):
    return render_template('light_sensor.html', ip = address, num = num, date = date)

@app.route('/make_graph/<which>/<num>/<start>/<end>')
def make_graph(which, num, start, end):
    '''
       make_graph route
         not rendered as full page, but used with AJAX in order to update page
         dynamically
    '''
    start = start.replace('T', ' ')
    end = end.replace('T', ' ')
    start = datetime.datetime.strptime(start, "%Y-%m-%d %H:%M").strftime("%m-%d-%y %H:%M:%S")
    end = datetime.datetime.strptime(end, "%Y-%m-%d %H:%M").strftime("%m-%d-%y %H:%M:%S")
    # uses which in order to create custom select sql query, as well as plot labels
    if which == 't':
        name = "Temperature Data"
        ylabel = "Temperature"
        sql = "SELECT Celsius, Date FROM Temperature WHERE Date BETWEEN '" + start + "' AND '" + end + "' AND ID = " +  num
    elif which == 'h':
        name = "Humidity Data"
        ylabel = "Humidity"
        sql = "SELECT Humidity, Date FROM Humidity WHERE Date BETWEEN '" + start + "' AND '" + end + "' AND ID = " + num 
    elif which == 'm':
        name = "Moisture Data"
        ylabel = "Moisture"
        sql = "SELECT Moisture, Date FROM Moisture WHERE Date BETWEEN '" + start + "' AND '" + end + "' AND ID = " +  num 
    elif which == 'n':
        name = "Light Intensity Data"
        ylabel = "Light Intensity"
        sql = "SELECT Light, Date FROM Light WHERE Date BETWEEN '" + start + "' AND '" + end + "' AND ID = " +  num 
    else:
        name = "UV Index"
        ylabel = "UV Index"
        sql = "SELECT UVIndex, Date FROM UV WHERE Date BETWEEN '" + start + "' AND '" + end + "' AND ID = " +  num 

    db = sqlite3.connect("/home/pi/project_green/Database/GreenhouseSensors")
    c = db.cursor()
        
    c.execute(sql)
    rows = c.fetchall()

    c.close()
    db.close()

    data,str_dates = zip(*rows)
    dates = [datetime.datetime.strptime(date, "%m-%d-%y %H:%M:%S") for date in str_dates]

    mat_dates = dts.date2num(dates)

    fig, ax = plt.subplots()

    fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')

    ax.set(xlabel='Date/Time', ylabel=ylabel, title=name)
    ax.grid()

    ax.plot_date(mat_dates, data)


    url = "images/graphs/dates.png"
    fig.savefig("static/" + url)
    return render_template('graph.html', url = url)


@app.route('/make_table/<which>/<start>/<end>')
def make_table(which, start, end):
	'''
	    make_graph route
		 not rendered as full page, but used with AJAX in order to update page
		 dynamically
	'''

	# uses which in order to create custom select sql query, as well as plot labels
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

	# connects to database and retrieves data (put in rows)
	db = sqlite3.connect("/home/pi/project_green/Database/GreenhouseSensors")
	c = db.cursor()
	
	c.execute(sql)
	rows = c.fetchall()

	c.close()
	db.close()

	# data is created derictly from rows
	data = np.array(rows)

	# compact rows together for table
	for row in data:
		cell_Text.append(row)

	# creates table
	table = plt.table(cellText = cell_Text,colLabels = ('Range', 'Measurement'),loc='center')

	plt.axis('off')
	plt.grid('off')
	
	url = "images/tables/table.png"
	fig.savefig("static/" + url)
	
	return render_template('table.html', url = url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
