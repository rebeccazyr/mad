import chromadb
from chromadb import PersistentClient

# 连接到ChromaDB
client = PersistentClient(path="./chroma/chroma_store")

# 列出所有collections
collections = client.list_collections()
print("Available collections:")
for coll in collections:
    print(f"- {coll.name}")

# 获取evidence_bgebase collection
try:
    collection = client.get_collection(name="evidence_bgebase")
    print(f"\nCollection '{collection.name}' found!")
    print(f"Collection count: {collection.count()}")
    
    # 尝试获取一些样本数据
    if collection.count() > 0:
        sample = collection.peek(limit=1)
        print(f"Sample data: {sample}")
    
except Exception as e:
    print(f"Error getting collection: {e}")

# 尝试直接创建collection，看看会发生什么
print("\nTrying to create/get collection with BAAI/bge-base-en-v1.5...")
try:
    from chroma.chroma import SentenceTransformerEmbeddingFunction
    collection2 = client.get_or_create_collection(
        name="evidence_bgebase_test",
        embedding_function=SentenceTransformerEmbeddingFunction()
    )
    print("Successfully created test collection!")
except Exception as e:
    print(f"Error creating collection: {e}")
    import traceback
    traceback.print_exc() 