from flask import Flask, render_template, make_response
from io import StringIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
	return render_template("wtfTest.html")
	
@app.route('/testGraph')
def testGraph():
	x = [1,2,3,4,5]
	y = [0,2,1,3,4]

	plt.plot(x,y)

	return plt.show()
	
	#img = StringIO.StringIO()
	#y = [1,2,3,4,5]
	#x = [0,2,1,3,4]
	
	#plt.plot(x,y)
	#plt.savefig(img, format='png')
	#img.seek(0)
	
	#plot_url = base64.b64encode(img.getvalue())

	#return render_template("wtfTest.html", plot_url=ploturl)

@app.route("/simple.png")
def simple():
	import datetime
	#import StringIO
	from io import BytesIO
	import random

	from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
	from matplotlib.figure import Figure
	from matplotlib.dates import DateFormatter

	fig=Figure()
	ax=fig.add_subplot(111)
	x=[]
	y=[]
	now=datetime.datetime.now()
	delta=datetime.timedelta(days=1)
	
	for i in range(10):
		x.append(now)
		now+=delta
		y.append(random.randint(0, 1000))
		
	ax.plot_date(x, y, '-')
	ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
	fig.autofmt_xdate()
	canvas=FigureCanvas(fig)
	#png_output = StringIO.StringIO()
	png_output = BytesIO()
	canvas.print_png(png_output)
	response=make_response(png_output.getvalue())
	response.headers['Content-Type'] = 'image/png'
	return response
	
if __name__ == "__main__":
	app.run(debug=True)