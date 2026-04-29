import ollama

chat_history = []
print("Starting chat. Type 'exit' to quit.")

MODEL="qwen:1.8b"

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit': break
        
    chat_history.append({'role': 'user', 'content': user_input})
    
    # The ollama library automatically targets localhost:11434
    response = ollama.chat(model=MODEL, messages=chat_history)
    
    print(f"AI: {response['message']['content']}\n")
    chat_history.append(response['message'])
