from chroma.chroma import ChromaClient
from agents.intent_word_enhanced_retrieval_points import intent_enhanced_reformulation
import json
from tqdm import tqdm
import os

# Initialize ChromaDB client
chroma_client = ChromaClient(vector_name="evidence_bgebase", path="/home/yirui/mad/chroma/chroma_store")

with open("test.json", "r") as f:
    all_examples = json.load(f)

output_file = "intent_enhanced_retrieved_simple_10_each_evidence_with_keywords_points.json"

if os.path.exists(output_file):
    with open(output_file, "r") as f:
        example_to_retrieved_map = json.load(f)
    print(f"Loaded existing data with {len(example_to_retrieved_map)} examples")
else:
    example_to_retrieved_map = {}
    print("Starting fresh data collection")

def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

for example in tqdm(all_examples, desc="Processing examples"):
    example_id = example.get("example_id")
    if not example_id:
        print("Skipping example with missing ID")
        continue

    if example_id in example_to_retrieved_map:
        print(f"Skipping example {example_id} - already processed")
        continue

    claim = example.get("claim")
    if not claim:
        print(f"Skipping example {example_id} - no claim found")
        continue

    try:
        result = intent_enhanced_reformulation(claim)
        pro_queries = result["pro_queries"]
        con_queries = result["con_queries"]

        pro_evidence_ids = []
        for pro_query in pro_queries:
            pro_results = chroma_client.query(query_text=pro_query, top_k=10, include=["metadatas"])
            pro_evidence_ids.extend([meta["evidence_id"] for meta in pro_results["metadatas"][0]])

        con_evidence_ids = []
        for con_query in con_queries:
            con_results = chroma_client.query(query_text=con_query, top_k=10, include=["metadatas"])
            con_evidence_ids.extend([meta["evidence_id"] for meta in con_results["metadatas"][0]])

        example_to_retrieved_map[example_id] = {
            "intent": result["intent"],
            "keywords": result["keywords"],
            "pro_queries": pro_queries,
            "con_queries": con_queries,
            "pro_evidence_ids": pro_evidence_ids,
            "con_evidence_ids": con_evidence_ids
        }

        save_to_json(example_to_retrieved_map, output_file)
        print(f"Processed and saved example {example_id}")

    except Exception as e:
        print(f"Error processing example {example_id}: {str(e)}")
        save_to_json(example_to_retrieved_map, output_file)
        continue

print(f"Processing completed. Total examples processed: {len(example_to_retrieved_map)}")
