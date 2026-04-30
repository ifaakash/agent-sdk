import requests
import chromadb

# ==========================================
# 1. Connect to your Local Database
# ==========================================
# Connect to the exact same folder we used in the ingest script
client = chromadb.PersistentClient(path="./local_vectordb")
collection = client.get_collection(name="color_guide")

# ==========================================
# 2. Helper Functions
# ==========================================
def get_embedding(text):
    """Converts the user's question into a vector using the same model."""
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "nomic-embed-text",
        "prompt": text
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["embedding"]

def generate_answer(prompt_text):
    """Sends the final assembled prompt to Qwen:1.8b and gets the answer."""
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "qwen:1.8b",
        "prompt": prompt_text,
        "stream": False # Set to True if you want it to type out word-by-word
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["response"]

# ==========================================
# 3. Main RAG Logic
# ==========================================
def ask_question(user_question):
    print(f"\n[1] Question: {user_question}")
    
    # Step A: Convert the user's question to a vector
    print("[2] Embedding your question...")
    question_vector = get_embedding(user_question)
    
    # Step B: Search ChromaDB for the closest matches
    print("[3] Searching local database for context...")
    results = collection.query(
        query_embeddings=[question_vector],
        n_results=2 # Grab the top 2 most relevant chunks
    )
    
    # Extract the actual text documents from the search results
    retrieved_chunks = results['documents'][0]
    
    if not retrieved_chunks:
        print("No relevant context found in the database.")
        return
    
    # Combine the chunks into a single string
    context = " ".join(retrieved_chunks)
    print(f"\n--- Retrieved Context ---\n{context}\n-------------------------\n")
    
    # Step C: Assemble the final prompt for Qwen
    print("[4] Assembling prompt and asking Qwen:1.8b...")
    final_prompt = f"""You are a helpful engineering assistant. 
    Use ONLY the following context to answer the user's question. If the answer is not in the context, say "I don't know based on the provided notes."
    
    Context:
    {context}
    
    Question:
    {user_question}
    """
    
    # Step D: Get the final answer
    answer = generate_answer(final_prompt)
    print(f"\n[Qwen:1.8b Answer]:\n{answer}\n")

# ==========================================
# 4. Run It!
# ==========================================
if __name__ == "__main__":
    # You can change this question to test it out!
    my_question = "What is red plus blue equal to ( answer in 3-4 words ) Also, what are the alternate name to the answer?"
    ask_question(my_question)
