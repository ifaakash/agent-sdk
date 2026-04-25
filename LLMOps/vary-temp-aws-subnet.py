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

OLLAMA_URL="http://localhost:11434/api/generate"
PROMPT="What is the difference between private and public subnet in AWS? Explain in 3 lines"
MODEL="qwen:0.5b"

temperatures=[0.1,0.7,1.5]
top_p=0.9

print(f"Testing Model: {MODEL}\nPrompt: '{PROMPT}'\n" + "-"*50)

for temp in temperatures:
   payload={
    'prompt': PROMPT,
    'model': MODEL,
    'options': {
        'temperature': temp,
        'top_p': top_p 
    },
    'stream': False
   }

   start_time= time.time()
   response= requests.post(OLLAMA_URL,json=payload)
   latency=round(time.time() - start_time,2)

   if response.status_code == 200:
       result= response.json()
       print(f"Temperature:     {temp}")
       print(f"Latency:         {latency} s")
       print(f"Output:          {result['response']}")
   else:
        print(f"Error hitting API: {response.status_code}")
