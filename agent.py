"""
Curl is an HTTP Client
For llama.cpp the endpoint POST v1/chat/completions is stateless.
So every calls needs all the messages that has happened so far.
Being stateless or statefull is a property of an endpoint and not code
"""

import logging
import requests
from tools import *

# logging.basicConfig(level=logging.DEBUG)

url = "http://127.0.0.1:8080/v1/chat/completions"
SYSTEM_PROMPT = """You are an angry agent, never great and show anger!
You can use tools to perform whatever action you're told to do.
You can use read_file tool to read a file.
You can use write_file tool to write something to a file. 
It will replace the files current content with the new content, 
so if someone tells you to append a file, read that file first, 
then add new content to current content and then do a write."
"""

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

print("")
print("-"*10)
print("Hey! This is a locally hosted Qwen 2.5 7B Instruct model using llama.cpp (An inference enginer and runtime)")
print("This is a small harness around it")
print("Enter any message to chat!")
print("Enter exit / quit to terminate the session")
print("-"*10)
print("\n")

while True: # REPL Loop (Read Eval Print Loop)

    user_input = input(">>> ").strip()
    logging.debug(user_input)

    if(user_input == ""):
        continue

    if(user_input.lower() == "quit" or user_input.lower() == "exit" or user_input.lower() == "exit()"):
        break

    user_msg = {"role": "user", "content": user_input}
    messages.append(user_msg)

    while True:
        data = {
            "model": "local",
            "messages": messages,
            "tools": tools,
        }

        try:
            response = requests.post(url, json=data, timeout=120)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print("⚠️ There is some server issue! Please wait for some time, for the server to be up back again")
            if messages[-1]["role"] == "user":
                messages.pop()
            break

        if response.status_code != 200:
            print("⚠️ There is some server issue! Please wait for some time, for the server to be up back again")
            if messages[-1]["role"] == "user":
                messages.pop()
            logging.debug(response.text)
            break

        assistant_msg = response.json()["choices"][0]["message"]
        logging.debug(assistant_msg)
        messages.append(assistant_msg)

        tool_calls = assistant_msg.get("tool_calls")
        print(assistant_msg.get("content"))

        if not tool_calls:
            break

        for tool_call in tool_calls:

            tool_call_id = tool_call["id"]
            content = execute(tool_call)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call_id,
                    "content": content,
                }
            )