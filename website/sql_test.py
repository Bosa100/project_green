import sqlite3
import matplotlib.dates as dt
from datetime import datetime


sql = "SELECT Moisture, Date FROM Moisture WHERE rowid BETWEEN 0 AND 5"

db = sqlite3.connect("/home/pi/project_green/Database/GreenhouseSensors")
c = db.cursor()
    
c.execute(sql)
rows = c.fetchall()

c.close()
db.close()


a,b = zip(*rows)
print(a)
print(b)

dates = [datetime.strptime(date, "%I:%M:%S%p on %B %d, %Y") for date in b]
print(dates)
