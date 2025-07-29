from chroma.chroma import ChromaClient
from agents.intent_enhanced_retrieval import intent_enhanced_reformulation
import json
from tqdm import tqdm
import os

# Initialize ChromaDB client
chroma_client = ChromaClient(vector_name="evidence_bilingual_large", path="/home/yirui/mad/chroma/chroma_store")

# Load test claims
with open("/home/yirui/mad/dataset/test_400.json", "r") as f:
    all_examples = json.load(f)

# Output file path
output_file = "/home/yirui/mad/bilin/intent_enhanced_bilingual_retrieved_each10_evidence.json"

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
        pro_claim = result["reformulated_pro"]
        con_claim = result["reformulated_con"]

        # Step 2: Query ChromaDB using pro_claim
        pro_results = chroma_client.query(query_text=pro_claim, top_k=10, include=["documents", "metadatas"])
        pro_evidence_ids = [meta["evidence_id"] for meta in pro_results["metadatas"][0]]

        # Step 3: Query ChromaDB using con_claim
        con_results = chroma_client.query(query_text=con_claim, top_k=10, include=["documents", "metadatas"])
        con_evidence_ids = [meta["evidence_id"] for meta in con_results["metadatas"][0]]

        # Step 4: Save to map
        example_to_retrieved_map[example_id] = {
            "intent": result["intent"],
            "pro_claim": pro_claim,
            "con_claim": con_claim,
            "pro_evidence_ids": pro_evidence_ids,
            "con_evidence_ids": con_evidence_ids
        }

        # Step 5: Save to file immediately
        save_to_json(example_to_retrieved_map, output_file)
        print(f"Processed and saved example {example_id}")
        
    except Exception as e:
        print(f"Error processing example {example_id}: {str(e)}")
        # Save current state even if there's an error
        save_to_json(example_to_retrieved_map, output_file)
        continue

print(f"Processing completed. Total examples processed: {len(example_to_retrieved_map)}")