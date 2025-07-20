from chroma import ChromaClient
import json
import numpy as np
from tqdm import tqdm

def analyze_similarity_scores():
    """分析ChromaDB查询的相似度分数"""
    
    # 初始化ChromaDB客户端
    chroma_client = ChromaClient(vector_name="evidence_bgebase")
    
    # 加载测试数据
    with open("dataset/test.json", "r") as f:
        all_examples = json.load(f)
    
    all_similarities = []
    all_distances = []
    
    print("分析相似度分数分布...")
    
    # 分析前10个示例的相似度分数
    for i, example in enumerate(tqdm(all_examples[:10], desc="Processing examples")):
        claim = example["claim"]
        example_id = example["example_id"]
        
        # 执行向量相似度搜索
        results = chroma_client.query(
            query_text=claim, 
            top_k=20, 
            include=["documents", "metadatas", "distances"]
        )
        
        distances = results["distances"][0]
        similarities = [1 - d for d in distances]
        
        all_distances.extend(distances)
        all_similarities.extend(similarities)
        
        print(f"\n示例 {i+1} (ID: {example_id}):")
        print(f"  查询: {claim[:100]}...")
        print(f"  前5个相似度分数: {similarities[:5]}")
        print(f"  平均相似度: {np.mean(similarities):.4f}")
        print(f"  最高相似度: {max(similarities):.4f}")
        print(f"  最低相似度: {min(similarities):.4f}")
    
    # 整体统计
    print("\n" + "="*60)
    print("整体相似度分数统计:")
    print(f"  总样本数: {len(all_similarities)}")
    print(f"  平均相似度: {np.mean(all_similarities):.4f}")
    print(f"  中位数相似度: {np.median(all_similarities):.4f}")
    print(f"  标准差: {np.std(all_similarities):.4f}")
    print(f"  最高相似度: {max(all_similarities):.4f}")
    print(f"  最低相似度: {min(all_similarities):.4f}")
    
    # 相似度分数分布
    print(f"\n相似度分数分布:")
    print(f"  > 0.9: {sum(1 for s in all_similarities if s > 0.9)} ({sum(1 for s in all_similarities if s > 0.9)/len(all_similarities)*100:.1f}%)")
    print(f"  0.8-0.9: {sum(1 for s in all_similarities if 0.8 <= s <= 0.9)} ({sum(1 for s in all_similarities if 0.8 <= s <= 0.9)/len(all_similarities)*100:.1f}%)")
    print(f"  0.7-0.8: {sum(1 for s in all_similarities if 0.7 <= s < 0.8)} ({sum(1 for s in all_similarities if 0.7 <= s < 0.8)/len(all_similarities)*100:.1f}%)")
    print(f"  0.6-0.7: {sum(1 for s in all_similarities if 0.6 <= s < 0.7)} ({sum(1 for s in all_similarities if 0.6 <= s < 0.7)/len(all_similarities)*100:.1f}%)")
    print(f"  < 0.6: {sum(1 for s in all_similarities if s < 0.6)} ({sum(1 for s in all_similarities if s < 0.6)/len(all_similarities)*100:.1f}%)")

def filter_by_similarity_threshold():
    """根据相似度阈值过滤结果"""
    
    chroma_client = ChromaClient(vector_name="evidence_bgebase")
    
    # 示例查询
    query_text = "COVID-19 transmission in restaurants"
    results = chroma_client.query(query_text=query_text, top_k=50)
    
    # 设置相似度阈值
    similarity_threshold = 0.7
    
    print(f"查询: {query_text}")
    print(f"相似度阈值: {similarity_threshold}")
    print("="*60)
    
    filtered_results = []
    
    for i, (doc, meta, distance) in enumerate(zip(
        results["documents"][0], 
        results["metadatas"][0], 
        results["distances"][0]
    )):
        similarity = 1 - distance
        
        if similarity >= similarity_threshold:
            filtered_results.append({
                "rank": i + 1,
                "document": doc,
                "metadata": meta,
                "distance": distance,
                "similarity": similarity
            })
    
    print(f"原始结果数: {len(results['documents'][0])}")
    print(f"过滤后结果数: {len(filtered_results)}")
    print(f"过滤率: {(1 - len(filtered_results)/len(results['documents'][0]))*100:.1f}%")
    
    print("\n过滤后的结果:")
    for result in filtered_results[:5]:  # 只显示前5个
        print(f"  排名 {result['rank']}: 相似度 {result['similarity']:.4f}")
        print(f"    文档: {result['document'][:80]}...")
        print(f"    元数据: {result['metadata']}")
        print()

if __name__ == "__main__":
    print("ChromaDB相似度分数分析")
    print("="*60)
    
    # 分析相似度分数分布
    analyze_similarity_scores()
    
    print("\n" + "="*60)
    
    # 根据阈值过滤结果
    filter_by_similarity_threshold() 