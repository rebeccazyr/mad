import chromadb
from chromadb import PersistentClient
import json

# 连接到ChromaDB
client = PersistentClient(path="./chroma/chroma_store")

# 获取collection
collection = client.get_collection(name="evidence_bgebase")

print("Collection info:")
print(f"Name: {collection.name}")
print(f"Count: {collection.count()}")

# 尝试获取collection的metadata
try:
    # 检查collection的属性
    print(f"Collection type: {type(collection)}")
    
    # 尝试获取一些内部信息
    if hasattr(collection, '_embedding_function'):
        print(f"Embedding function: {collection._embedding_function}")
    
    if hasattr(collection, 'metadata'):
        print(f"Collection metadata: {collection.metadata}")
    
    # 尝试直接查询，看看是否会出现错误
    print("\nTrying to query the collection...")
    results = collection.query(
        query_texts=["test query"],
        n_results=1
    )
    print("Query successful!")
    
except Exception as e:
    print(f"Error during query: {e}")
    import traceback
    traceback.print_exc()

# 检查ChromaDB的数据库文件
print("\nChecking ChromaDB database structure...")
import os
chroma_path = "./chroma/chroma_store"
if os.path.exists(chroma_path):
    print(f"ChromaDB path exists: {chroma_path}")
    for item in os.listdir(chroma_path):
        print(f"  - {item}")
        
    # 检查collection目录
    collection_dirs = [d for d in os.listdir(chroma_path) if os.path.isdir(os.path.join(chroma_path, d)) and d != '__pycache__']
    for coll_dir in collection_dirs:
        print(f"\nCollection directory: {coll_dir}")
        coll_path = os.path.join(chroma_path, coll_dir)
        if os.path.exists(coll_path):
            for item in os.listdir(coll_path):
                print(f"  - {item}") 