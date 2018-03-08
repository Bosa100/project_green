from flask import Flask, render_template
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

	plt.show()
	
	#img = StringIO.StringIO()
	#y = [1,2,3,4,5]
	#x = [0,2,1,3,4]
	
	#plt.plot(x,y)
	#plt.savefig(img, format='png')
	#img.seek(0)
	
	#plot_url = base64.b64encode(img.getvalue())

	#return render_template("wtfTest.html", plot_url=ploturl)
	
if __name__ == "__main__":
	app.run(debug=True)