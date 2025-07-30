from chroma.chroma import ChromaClient
import json
from tqdm import tqdm
import os

# Initialize ChromaDB client
chroma_client = ChromaClient(vector_name="evidence_bgebase", path="/home/yirui/mad/chroma/chroma_store/evidence_bgebase")

# Load test claims
with open("/home/yirui/mad/intent_enhanced_retrieved_simple_20_evidence.json", "r") as f:
    all_examples = json.load(f)

with open("/home/yirui/mad/chroma/test/example_to_claim.json", "r") as f:
    example_to_claim = json.load(f)

with open("/home/yirui/mad/single/retrieve/evidence_id_to_text.json", "r") as f:
    evidence_id_to_text = json.load(f)
print(f"Loaded {len(evidence_id_to_text)} evidence mappings")

# Output file
output_file = "intent_enhanced_bge_con_pro_bge_large_2000_top20_by_score.json"

# Load or initialize output map
if os.path.exists(output_file):
    with open(output_file, "r") as f:
        example_to_retrieved_map = json.load(f)
    print(f"Loaded existing data with {len(example_to_retrieved_map)} examples")
else:
    example_to_retrieved_map = {}
    print("Starting fresh")

def save_to_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

for example_id, example in tqdm(all_examples.items(), desc="Processing examples"):
    if example_id in example_to_retrieved_map:
        print(f"Skipping example {example_id} - already processed")
        continue

    try:
        claim = example_to_claim[example_id]
        intent = example["intent"]
        pro_claim = example["pro_claim"]
        con_claim = example["con_claim"]

        # Query ChromaDB
        pro_results = chroma_client.query_score(query_text=pro_claim, top_k=50, include=["metadatas", "distances"])
        con_results = chroma_client.query_score(query_text=con_claim, top_k=50, include=["metadatas", "distances"])

        # Merge results with score and source
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

        # Sort and deduplicate
        seen = set()
        top_20_ids = []
        top_20_text = []

        for item in sorted(combined, key=lambda x: x["score"]):
            if item["evidence_id"] not in seen:
                top_20_ids.append(item["evidence_id"])
                
                evidence_id_str = str(item["evidence_id"])
                if evidence_id_str in evidence_id_to_text:
                    top_20_text.append(evidence_id_to_text[evidence_id_str])
                else:
                    top_20_text.append("Evidence not found")
                
                seen.add(item["evidence_id"])
                
            if len(top_20_ids) == 20:
                break

        # Save result
        example_to_retrieved_map[example_id] = {
            "claim": claim,
            "intent": intent,
            "pro_claim": pro_claim,
            "con_claim": con_claim,  
            "top_20_evidences_ids": top_20_ids,
            "evidence_full_text": top_20_text
        }

        save_to_json(example_to_retrieved_map, output_file)
        print(f"Processed example {example_id}")

    except Exception as e:
        print(f"Error on {example_id}: {e}")
        save_to_json(example_to_retrieved_map, output_file)
        continue

print(f"All done. Total processed: {len(example_to_retrieved_map)}")