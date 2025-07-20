from chroma import ChromaClient

# 初始化 ChromaDB 客户端
chroma_client = ChromaClient(vector_name="evidence_bgebase")

# 测试搜索
claim = "The Earth is flat."
results = chroma_client.query(query_text=claim, top_k=5, include=["documents", "metadatas"])

print("搜索结果:")
print(f"找到 {len(results['documents'][0])} 个相关文档")

for i, (text, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
    print(f"TOP{i+1} : [证据ID: {meta['evidence_id']}]\n{text[:200]}...\n") 