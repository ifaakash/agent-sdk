'''
  Model
    architecture        qwen2    
    parameters          620M     
    context length      32768    
    embedding length    1024     
    quantization        Q4_0     
'''

import requests

OLLAMA_URL="http://localhost:11434/api/generate"
MODEL="qwen:0.5b"
TEMP=0.5

print(f"Starting chat with {MODEL}. Type 'quit' or 'exit' to stop.\n")

while True:
   PROMPT= input("Prompt: \n")
   if PROMPT.lower() in ['exit', 'quit']:
    print('Ending chat, Goodbye!')
    break

   payload={
    "model": MODEL,
    "prompt": PROMPT,
    "stream": False,
    "options": {
    "temperature": TEMP
    }
   }

   try:
     response= requests.post(OLLAMA_URL, json=payload)
  
     if response.status_code == 200:
        print("*"*50)
        result= response.json()
        print(f"Response:\n{result['response']}")
        print("*" * 50 + "\n")
     else:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)
   except requests.exceptions.ConnectionError:
         print("\nError: Could not connect to Ollama. Make sure the Ollama app is running locally!")
         break
