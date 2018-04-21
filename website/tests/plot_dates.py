import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import numpy as np

date1 = datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S.%f")
date2 = datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S.%f")
date3 = datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S.%f")
date4 = datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S.%f")
date5 = datetime.datetime.now().strftime("%m/%d/%y %I:%M:%S.%f")

dates = [date1, date2, date3, date4, date5]
mat_dates = [datetime.datetime.strptime(date, "%m/%d/%y %I:%M:%S.%f") for date in dates]
print(dates)


values = [3, 4, 5, 6, 7]

mat_dates = dts.date2num(mat_dates)

fig, ax = plt.subplots()
ax.plot_date(mat_dates, values)

ax.set(xlabel='Date Times', ylabel="Value", title="Sample Dates")
ax.grid()

url = "images/graphs/dates.png"
fig.savefig("static/" + url)

