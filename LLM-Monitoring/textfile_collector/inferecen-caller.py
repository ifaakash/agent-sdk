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
PROMPT="What is internet Gateway in AWS?"

temperatures= [0.7]

for temp in temperatures:
   
