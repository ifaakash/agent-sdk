import os
import requests
import chromadb

# ==========================================
# 1. Database Setup
# ==========================================
# PersistentClient saves the vector DB to a folder on your local disk
client = chromadb.PersistentClient(path="./local_vectordb")

# Collections are like tables in SQL. We'll create one for your notes.
collection = client.get_or_create_collection(name="devops_notes")

# ==========================================
# 2. Helper Functions
# ==========================================
def chunk_text(text, chunk_size=300, overlap=50):
    """Breaks large text into smaller chunks with a slight overlap."""
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

def get_embedding(text):
    """Calls local Ollama to convert text into a vector."""
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": "nomic-embed-text",
        "prompt": text
    }
    response = requests.post(url, json=payload)
    response.raise_for_status() # Ensure the request was successful
    return response.json()["embedding"]

# ==========================================
# 3. Main Ingestion Flow
# ==========================================
def ingest_file(filepath):
    print(f"Reading {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Step A: Chunk the document
    chunks = chunk_text(content)
    print(f"Broke file into {len(chunks)} chunks.")

    # Step B & C: Embed and Store
    for i, chunk in enumerate(chunks):
        print(f"Embedding chunk {i+1}/{len(chunks)}...")
        vector = get_embedding(chunk)

        # Store the chunk, its vector, and metadata in ChromaDB
        collection.add(
            documents=[chunk],                  # The actual readable text
            embeddings=[vector],                # The numerical representation
            metadatas=[{"source": filepath}],   # Metadata to track where it came from
            ids=[f"{filepath}_chunk_{i}"]       # A unique ID for the chunk
        )
    print("Ingestion complete! Data safely stored in ChromaDB.")

# ==========================================
# 4. Run the Pipeline
# ==========================================
if __name__ == "__main__":
    # Create a dummy documentation file for testing
    test_filename = "aws_networking.txt"
    with open(test_filename, "w") as f:
        f.write("A public subnet is a subnet that has a route in its route table pointing to an Internet Gateway (IGW). ")
        f.write("This allows resources within the subnet, like an ALB, to communicate directly with the internet. ")
        f.write("A private subnet, on the other hand, does not have a route to the IGW. It must use a NAT Gateway to access the internet.")
    
    # Run the ingestion
    ingest_file(test_filename)
