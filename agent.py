"""
Curl is an HTTP Client
For llama.cpp the endpoint POST v1/chat/completions is stateless.
So every calls needs all the messages that has happened so far.
Being stateless or statefull is a property of an endpoint and not code
"""

from email import message
import requests

url = "http://127.0.0.1:8080/v1/chat/completions"
SYSTEM_PROMPT = "You are a angry agent, never great and show anger!"

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("\n")
print("-"*10)
print("Hey! This is a locally hosted Qwen 2.5 7B Instruct model using llama.cpp (An inference enginer and runtime)")
print("This is a small harness around it")
print("Enter any message to chat!")
print("Enter exit / quit to terminate the session")
print("-"*10)
print("\n")

while True:

    user_input = input(">>>")

    if(user_input.lower() == "quit" or user_input.lower() == "exit" or user_input.lower() == "exit()"):
        break

    user_msg = {"role": "user", "content": user_input}
    messages.append(user_msg)

    data = {
        "messages": messages
    }

    response = requests.post(url, json=data).json()
    assistant_msg = response["choices"][0]["message"]
    print(response["choices"][0]["message"]["content"])

    messages.append(assistant_msg)



