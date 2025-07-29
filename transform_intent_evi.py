import json

# Load input JSON
with open("/home/yirui/mad/bilin/intent_enhanced_bilingual_retrieved_each10_evidence.json", "r") as f:
    raw_data = json.load(f)

with open("/home/yirui/mad/single/retrieve/evidence_id_to_text.json", "r") as f:
    evidence_id_to_text = json.load(f)

with open("/home/yirui/mad/chroma/test/example_to_claim.json", "r") as f:
    example_to_claim = json.load(f)

merged_data = {}
print(len(raw_data))
for i, (key, entry) in enumerate(raw_data.items()):
    pro_ids = entry.get("pro_evidence_ids", [])
    con_ids = entry.get("con_evidence_ids", [])
    # top_20_evidences = entry.get("top_20_evidences", [])
    # top_20_evidences = entry
    merged_ids = list(set(pro_ids + con_ids))
    claim = example_to_claim[key]
    # Convert integer IDs to strings to match the dictionary keys
    evidence_full_text = [evidence_id_to_text[str(id)] for id in merged_ids]
    # evidence_full_text = [f"[{idx+1}] {evidence_id_to_text[str(id)]}" for idx, id in enumerate(top_20_evidences)]
    # evidence_pro_text = [evidence_id_to_text[str(id)] for id in pro_ids]
    # evidence_con_text = [evidence_id_to_text[str(id)] for id in con_ids]
    merged_data[key] = {
        "claim": claim,
        "evidence_full_text": evidence_full_text
    }

with open("/home/yirui/mad/bilin/intent_enhanced_bilingual_retrieved_each10_evidence_with_evi.json", "w") as f:
    json.dump(merged_data, f, indent=2)