import sqlite3
from datetime import datetime 
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import numpy as np


sql = "SELECT Moisture, Date FROM Moisture WHERE rowid BETWEEN 0 AND 100"

db = sqlite3.connect("/home/pi/project_green/Database/GreenhouseSensors")
c = db.cursor()
    
c.execute(sql)
rows = c.fetchall()

c.close()
db.close()


data,str_dates = zip(*rows)

dates = [datetime.strptime(date, "%m-%d-%y %H:%M:%S") for date in str_dates]

mat_dates = dts.date2num(dates)

for date in dates:
    print(date)

fig, ax = plt.subplots()

fig.autofmt_xdate(bottom=0.2, rotation=30, ha='right')

ax.set(xlabel='Date Times', ylabel="Value", title="Sample Dates")
ax.grid()

ax.plot_date(mat_dates, data)


url = "images/graphs/dates.png"
fig.savefig("static/" + url)

