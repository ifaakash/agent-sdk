# running qwen:0.5B model with 620M parameters
# This model has Q4_0 quantization
'''
  Model
    architecture        qwen2    
    parameters          620M     
    context length      32768    
    embedding length    1024     
    quantization        Q4_0   
'''

import requests
import time
# importing ollama is not required, as this script will make the API call externally, not locally
# from ollama import chat 

OLLAMA_URL="http://localhost:11434/api/generate"
MODEL="qwen:0.5b"
PROMPT="Write a creative, one-sentence tagline for a new cloud computing company"

# robotic (0.1), balanced (0.7), and chaotic (1.5) temperature
temperatures=[0.1, 0.7, 1.5]

print(f"Testing Model: {MODEL}\nPrompt: '{PROMPT}'\n" + "-"*50)

for temp in temperatures:
    payload= {
        'model': MODEL,
        'prompt': PROMPT,
        'format': "json",
        'options': {
            "temperature": temp,
            "top_p": 0.9
        },
        "stream": False
    }
    start_time = time.time()
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
