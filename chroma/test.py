from chroma import ChromaClient

client = ChromaClient(vector_name="evidence_bgebase")
data = client.collection.get()
print("data length of chromadb", len(data['ids']))

for i in range(min(5, len(data['ids']))):
    print(f"ID: {data['ids'][i]}")
    print(f"context: {data['documents'][i]}")
    print(f"metadata: {data['metadatas'][i]}")
    print("------")

