from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from openai import OpenAI
key = ""  #TODO: INSERT API KEY
client = OpenAI(api_key=key)
def assistant_message(m:str):
    return {"role": "assistant", "content":m}
def user_message(m:str):
    return {"role": "user", "content":m}

point_of_interest = ""

context:list[dict] = [
    assistant_message("""
        You are a professional and friendly surveyor.
        You will ask one question at a time and include emojis to maintain a friendly tone.
        You will respond only with one singular question, avoiding general questions.
        You will keep asking relevant questions based on the user's previous responses, prioritizing a variety of topics rather than focusing too deeply on one.
        When the user responds to a question, you will ask a follow-up question that explores a different aspect of their experience. Avoid asking multiple questions about the same detail.

        For example:
        - Question: How would you rate the overall taste of the ice cream?
        - User response: It was good.
        - Follow-up question: What did you think about the variety of flavors we offer?

        If you run out of direct follow-up questions, ask a relevant question from another part of the survey.

        Here is the user's previous questionnaire:
        Question 1: How was the customer service?
        User response: Good
        Question 2: Would you recommend our shop to your friends?
        User response: No
        Question 3: What part of the shop attracts you the most?
        User response: Location
        Question 4: How were the burgers?
        User response: Tasty

        Your task is to continue asking questions based on these responses without focusing too deeply on a single topic. Keep the questions varied and engaging. For example:

        - Question: What do you think about the cleanliness of our shop?
        - Question: How did you find the pricing of our products?
        - Question: What did you think about the waiting time for your order?
        - Question: How was the atmosphere in our shop?
        - Question: What would you suggest to improve our customer service? 
        - Question: How did you hear about our shop?
                      
        You will respond with only one question. One singular question while keeping in mind the limits.
        You will not speed for more than 2 sentences.
    """
    ),
]

dialogue : list[tuple] = []

def generate_question()->str:
    new_question = client.chat.completions.create(
        model = 'gpt-3.5-turbo-16k',
        messages=context
    ).choices[0].message.content
    context.append(assistant_message(new_question))
    return new_question

def generate_initial_question(questionnaire_result:str, point_of_interest:str)->str:
    #update the prompt
    context.append(assistant_message(f"Here is the result of the questionnaire {questionnaire_result}, you will form your quesions around the questionnaire"))
    context.append(assistant_message(f"In addition, your question should gear toward the point of interest: {point_of_interest}"))

    init_question = client.chat.completions.create(
        model = 'gpt-3.5-turbo-16k',
        messages = context
    ).choices[0].message.content

    # append question to context
    context.append(assistant_message(init_question))
    print(init_question, type(init_question))
    return init_question

app = Flask(__name__)
CORS(app)

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
    print(pointOfInterest)
    point_of_interest = pointOfInterest  # Keep this
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
    return jsonify(generate_initial_question(questionaire, point_of_interest)), 200

@app.route("/submit_ai_response", methods = ["POST"])
def additional_survey_form() -> str:
    data = request.json
    user_response = data.get("answer")
    # append user_reponse to the context
    context.append(user_message(user_response))
    question = generate_question()
    return jsonify(question), 200

if __name__ == '__main__':
    app.run(port=8000)

