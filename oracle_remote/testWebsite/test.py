from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hope')
def hello_potato():
    return 'There is no hope'

@app.route('/potato/<name>')
def print_name(name):
    return "your name is :{0}".format(name);

app.run(host= '0.0.0.0', port=5000, debug=False)
