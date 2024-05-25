from flask import Flask,request, render_template
app = Flask(__name__)

@app.route('/')
def index()
    return render_template('index.html')

@app.route('/submit_form', methods = ['POST'])
def submit_form