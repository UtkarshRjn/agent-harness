"""
Curl is an HTTP Client
For llama.cpp the endpoint POST v1/chat/completions is stateless.
So every calls needs all the messages that has happened so far.
Being stateless or statefull is a property of an endpoint and not code
"""


import json
import logging
import requests
import tools

# logging.basicConfig(level=logging.DEBUG)

url = "http://127.0.0.1:8080/v1/chat/completions"
SYSTEM_PROMPT = """
You are an angry agent, never great and show anger!
You can use tools to perform whatever action you're told to do.
You can use read_file tool to read a file.
"""

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
            "tools": tools.tools,
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
        if not tool_calls:
            print(assistant_msg.get("content"))
            break

        for tool_call in tool_calls:
            tool_call_id = tool_call["id"]
            func_name = tool_call["function"]["name"]

            if func_name not in tools.TOOL_REGISTRY:
                content = "Error: unknown tool: " + func_name
            else:
                try:
                    func_args = json.loads(tool_call["function"]["arguments"])
                    content = tools.TOOL_REGISTRY[func_name](**func_args)
                except Exception as e:
                    content = f"Tool error: {e}"

            print("Tool Call:", func_name)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": content,
            })


