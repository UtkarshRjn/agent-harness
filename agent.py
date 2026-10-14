"""
Curl is an HTTP Client
For llama.cpp the endpoint POST v1/chat/completions is stateless.
So every calls needs all the messages that has happened so far.
Being stateless or statefull is a property of an endpoint and not code
"""

import requests

url = "http://127.0.0.1:8080/v1/chat/completions"
SYSTEM_PROMPT = "You are a angry agent, never great and show anger!"

data = {
    "messages": [
      {"role": "system", "content": SYSTEM_PROMPT},
      {"role": "user", "content": "Say hello in one sentence."}
    ]
  }

response = requests.post(url, json=data).json()

print(response)
# print(response["choices"][0]["message"]["content"])

