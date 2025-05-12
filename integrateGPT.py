from puter import ChatCompletion
from dotenv import load_dotenv
import os
import json
from dataHandling import get_all_data


def get_prompt(convo, data):
    prompt = f"""You are an AI assistant helping students with quiz questions.

Instructions:
1. Read the JSON data enclosed in @ symbols.
2. Identify the correct question based on the user’s mention of the question number, no need to repeat the question and option in the response just give prompt ans and reason.
3. If no question number is mentioned, reply: "Please specify the question."

@{json.dumps(data, indent=2)}@

Conversation:
Student: {convo}
You (doubt_solving_ai):
"""
    return prompt

load_dotenv()
api = os.getenv("GPT_API_KEY")

def askGPT(prompt):
    response = ChatCompletion.create(
        messages=[{"role": "user", "content": prompt}],
        model="gpt-4o",
        driver="openai-completion",
        api_key=str(api)
    )
    print(json.dumps(response, indent=4, sort_keys=True))

    return response["result"]["message"]["content"]

def askDoubt(convo, unique_code:str):
    try:
        data = get_all_data(unique_code)

    except FileNotFoundError:
        print("FileNotFoundError")

    prompt = get_prompt(convo, data)
    response = askGPT(prompt)

    return response

