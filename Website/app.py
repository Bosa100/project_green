from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cakes')
def cake():
    return 'Yummy cakes!'

@app.route('/json')
def getJson():
    import json
    import urllib.request 
    res = urllib.request.urlopen("http://10.0.192.62:3000")
    json_str = res.read()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')



