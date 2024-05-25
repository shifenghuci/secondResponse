import streamlit as st

# parameter
MAX_DEPTH = 5 # Restrict round of dialogue with AI to 5




st.title("Prototype for secondResponse, demo only")

# Later include in prompt to craft contextual questions
pt_interest = st.text_area("Enter point of interest separated by space: ")

interests = pt_interest.split(' ')
interests

responses:list = []
if interests:
    # Gather pre-written questionnaire
    questions = st.text_area("Enter your pre-written questions separated by empty line:")
    for i, question in enumerate(questions.split('\n')):
        responses.append(st.text_area(f"Question {i}: {question}"))

# Check if all questions has been answered
def isComplete(responses:list)->bool:
    if all(x for x in responses):
        return True
    else:
        st.error("Please respond to all quesitons")
        return False

responses
# Confirm submission, response feed to openAI
submit = st.button("Submit my response")

# Enter AI dialogue parts
if isComplete(responses) and submit:
    st.header("AI questions below")
    # Formula prompt
    
    count = 0
    while count != MAX_DEPTH:
        
        # Prompt openAI to generate first questions

        # Waiting for user input

        count += 1
        # Prompt open AI to generate second questions

        # Repeat until max_depth reach
