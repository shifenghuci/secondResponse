from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/submit', methods = ['POST'])
def submit_form():
    data = request.form
    pointOfInterest = data.get('pointOfInterest')
    preDeterminedQuestions = data.get('preDeterminedQuestions')



    print(pointOfInterest)
    print(preDeterminedQuestions)
    return jsonify(pointOfInterest,preDeterminedQuestions), 200

if __name__ == '__main__':
    app.run(port=8000)
