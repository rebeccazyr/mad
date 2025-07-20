import sys
sys.path.append("./chroma")

from chroma import ChromaClient

# 测试修复后的ChromaClient
print("Testing fixed ChromaClient...")
chroma_client = ChromaClient(vector_name="evidence_bgebase")

# 测试查询
print("\nTesting query...")
claim = "The Earth is flat."
results = chroma_client.query(query_text=claim, top_k=5, include=["documents", "metadatas"])

print(f"Query successful! Found {len(results['documents'][0])} results")
for i, (text, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
    print(f"TOP{i+1} : [{meta['evidence_id']}]\n{text[:100]}...\n") 