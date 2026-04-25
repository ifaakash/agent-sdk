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

from ollama import chat

messages = [
    {
        'role' : 'user',
        'content': 'hey ollama! My name is Aakash'
    }
]
response = chat(
    model="qwen:0.5b", messages=messages, options={"temperature":1.5}
)

print("The model response is: ")
# print(type(response))
print(response.message.content)
