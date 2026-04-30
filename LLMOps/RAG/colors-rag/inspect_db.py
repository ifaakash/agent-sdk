import chromadb
import json

# Connect to the existing local database
client = chromadb.PersistentClient(path="./local_vectordb")
collection = client.get_collection(name="color_guide")

# 1. Check total item count
count = collection.count()
print(f"Total chunks stored: {count}\n")

# 2. View all stored documents and metadata (without printing the massive vectors)
results = collection.get(
    include=["documents", "metadatas"] # Exclude "embeddings" so it doesn't flood the terminal
)

# Print the results nicely
for i in range(count):
    print(f"--- Document {i+1} ---")
    print(f"ID: {results['ids'][i]}")
    print(f"Metadata: {results['metadatas'][i]}")
    print(f"Text: {results['documents'][i]}\n")
