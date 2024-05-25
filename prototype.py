import streamlit as st

st.title("Prototype for secondResponse, demo only")

# Includelater in prompt to craft contextual questions
pt_interest = st.text_area("Enter point of interest separated by space: ")

interests = pt_interest.split(' ')
interests

responses:list = []
if interests:
    questions = st.text_area("Enter your pre-written questions separated by empty line:")
    for i, question in enumerate(questions.split('\n')):
        responses.append(st.text_area(f"Question {i}: {question}"))

def isComplete(responses:list)->bool:
    if all(x for x in responses):
        return True
    else:
        st.error("Please respond to all quesitons")
        return False

responses
submit = st.button("Submit my response")
if isComplete(responses) and submit:
    st.header("AI questions below")
