from openai import OpenAI
client = OpenAI(api_key=open("API_KEY").read())
def assistant_message(m:str):
    return {"role": "assistant", "content":m}
def user_message(m:str):
    return {"role": "user", "content":m}


context:list[dict] = [
    assistant_message("You are a helpful assistant whose respond end with emoji"),
    assistant_message("You only ask question to user like a professional survey"),
    assistant_message("You should come up with at least 10 questions"),
    assistant_message("In addition, your question should gear toward the point of interest: matcha flavor"),
    assistant_message("You should try asking contextual and insightful question, but make sure you stick closely to point of interest"),
    assistant_message("Only ask free response question like an interview"),
    assistant_message("Try to have user explain their answer in more detail")
]

dialogue : list[tuple] = []
def generate_question()->str:
    return client.chat.completions.create(
        model = 'gpt-3.5-turbo-16k',
        messages=context
    ).choices[0].message.content

def generate_initial_question(questionnaire_result:str)->str:
    return client.chat.completions.create(
        model = 'gpt-3.5-turbo-16k',
        messages=[{"role" : "assistant", "content" : f"Here is the result of the questionnaire {questionnaire_result}"}]
        + [{"role": "assistant", "content" :"Based on the questionnaire and the user's response, ask a question as professional surveyor"}]
    ).choices[0].message.content

s = open('questionnaire_result.txt','r').read()
initial_question = generate_initial_question(s)
answer = input(f"{1}. {initial_question}\n")
dialogue.append((initial_question, answer))
context.append(assistant_message(initial_question))
context.append(user_message(answer))
for i in range(2,6):
    question = generate_question()
    answer = input(f"{i}. {question}\n")
    dialogue.append((question, answer))
    context.append(assistant_message(question))
    context.append(user_message(answer))

print("The survey end, thank you for taking the survey")