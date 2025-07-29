from chroma.chroma import ChromaClient
from agents.intent_word_enhanced_retrieval import intent_enhanced_reformulation
import json
from tqdm import tqdm
import os

# Initialize ChromaDB client
chroma_client = ChromaClient(vector_name="evidence_bilingual_large", path="/home/yirui/mad/chroma/chroma_store")

# Load test claims
with open("/home/yirui/mad/dataset/test_400.json", "r") as f:
    all_examples = json.load(f)

# Output file path
output_file = "intent_enhanced_400_con_only_retrieved_simple_20_evidence_with_keywords_score_ranked.json"

# Initialize output structure - load existing data if file exists
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        example_to_retrieved_map = json.load(f)
    print(f"Loaded existing data with {len(example_to_retrieved_map)} examples")
else:
    example_to_retrieved_map = {}
    print("Starting fresh data collection")

def save_to_json(data, filename):
    """Helper function to save data to JSON file"""
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

for example in tqdm(all_examples, desc="Processing examples"):
    example_id = example["example_id"]
    
    # Skip if already processed
    if example_id in example_to_retrieved_map:
        print(f"Skipping example {example_id} - already processed")
        continue
    
    claim = example["claim"]

    try:
        # Step 1: Infer intent and reformulate
        result = intent_enhanced_reformulation(claim)
        # pro_claim = result["reformulated_pro"]
        con_claim = result["reformulated_con"]

        # Step 2: Query ChromaDB with pro_claim and con_claim
        pro_results = chroma_client.query_score(query_text=claim, top_k=50, include=["metadatas", "distances"])
        con_results = chroma_client.query_score(query_text=con_claim, top_k=50, include=["metadatas", "distances"])

        # Step 3: Merge results with score and evidence_id
        combined = []

        for score, meta in zip(pro_results["distances"][0], pro_results["metadatas"][0]):
            combined.append({
                "evidence_id": meta["evidence_id"],
                "score": score,
                "source": "pro"
            })

        for score, meta in zip(con_results["distances"][0], con_results["metadatas"][0]):
            combined.append({
                "evidence_id": meta["evidence_id"],
                "score": score,
                "source": "con"
            })

        # Step 4: Sort by score (lower is better for distances) and deduplicate evidence_ids
        seen = set()
        top_20 = []
        for item in sorted(combined, key=lambda x: x["score"]):
            if item["evidence_id"] not in seen:
                top_20.append(item["evidence_id"])
                seen.add(item["evidence_id"])
            if len(top_20) == 20:
                break

        # Step 5: Save
        example_to_retrieved_map[example_id] = {
            "intent": result["intent"],
            "keywords": result["keywords"],
            # "pro_claim": pro_claim,
            "con_claim": con_claim,
            "top_20_evidences": top_20
        }

        save_to_json(example_to_retrieved_map, output_file)
        print(f"Processed example {example_id}")

    except Exception as e:
        print(f"Error on {example_id}: {e}")
        save_to_json(example_to_retrieved_map, output_file)
        continue

print(f"All done. Total processed: {len(example_to_retrieved_map)}")
