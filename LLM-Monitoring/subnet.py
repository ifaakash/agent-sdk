'''
  Model
    architecture        qwen2    
    parameters          2B       
    context length      32768    
    embedding length    2048     
    quantization        Q4_0     
'''

import requests
import time

OLLAMA_URL="http://localhost:11434/api/generate"
MODEL="qwen:1.8b"
PROMPT= input("Enter Prompt: ")
temperature= [0.7]
# context window of 8000 token ( 6000 words )
CTXW= 8000
print(f"Testing Model: {MODEL}\nPrompt: '{PROMPT}'\n" + "-"*50)

for temp in temperature:
    payload={
        'model': MODEL,
        'prompt': PROMPT, 
        'stream': False,
        'options': {
            'temperature' : temp,
            'num_ctx' : CTXW
        }
    }
    start_time= time.time()
    response = requests.post(OLLAMA_URL, json=payload)
    latency = round(time.time() - start_time, 2)
    if response.status_code == 200:
        result = response.json()
        print(f"Temperature: {temp}")
        print(f"Latency:     {latency}s")
        print(f"Output:      {result['response'].strip()}\n")
        print(f"Tokens:      {result['eval_count']}")
        print(f"Duration:    {result['eval_duration']/1000000000}s")
    else:
        print(f"Error hitting API: {response.status_code}")

