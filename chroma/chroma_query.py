from chroma import ChromaClient
import json
from tqdm import tqdm

# Initialize ChromaDB client with the same collection name used during insertion
chroma_client = ChromaClient(vector_name="evidence_bilingual_large")

# Input claim to retrieve evidence for
with open("test.json", "r") as f:
    all_examples = json.load(f)
example_to_retrieved_evidence_map = {}
for example in tqdm(all_examples, desc="Processing examples"):
    claim = example["claim"]
    example_id = example["example_id"]
    example_to_retrieved_evidence_map[example_id] = []
    # Perform vector similarity search
    results = chroma_client.query(query_text=claim, top_k=20, include=["documents", "metadatas"])
    # print(results)
    for i, (text, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        # print (claim)
        # print (text)
        # print (meta)
        example_to_retrieved_evidence_map[example_id].append(meta["evidence_id"])
    # break
    # print(example_to_retrieved_evidence_map)

# Save mapping to JSON
with open("20_test_retrieved_evidence_evidence_bilingual_large.json", "w") as f:
    json.dump(example_to_retrieved_evidence_map, f, indent=2)