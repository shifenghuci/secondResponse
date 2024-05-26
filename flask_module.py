from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/submit_index', methods = ['POST'])
def submit_index_form():
    data = request.form
    pointOfInterest = data.get('pointOfInterest')
     # preDeterminedQuestions = data.get('preDeterminedQuestions')

    print(pointOfInterest)
    # print(preDeterminedQuestions)
    return pointOfInterest, 200

@app.route('/submit_survey', methods = ['POST'])
def submit_survey_form():
    data = request.json  # Use request.json to get JSON data
    survey_responses = data.get("surveyResponses")
    print(survey_responses)
    # Print keys and values
    questionaire: str = ""
    for key, value in survey_responses.items():
        questionaire += f"{key}, Answer: {value}\n"
    print(questionaire)
    return questionaire, 200


if __name__ == '__main__':
    app.run(port=8000)
