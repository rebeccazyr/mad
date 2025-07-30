import json

# Load input JSON
# with open("/home/yirui/mad/intent_enhanced_score_merged_evidence_ids.json", "r") as f:
#     raw_data = json.load(f)

with open("/home/yirui/mad/single/retrieve/evidence_id_to_text.json", "r") as f:
    evidence_id_to_text = json.load(f)

with open("/home/yirui/mad/chroma/test/example_to_claim.json", "r") as f:
    example_to_claim = json.load(f)

with open("/home/yirui/mad/intent_enhanced_top20_by_score.json", "r") as f:
    raw_data = json.load(f)

# Remove this line that was causing the problem
# merged_data = {}
merged_data = {}
print(len(raw_data))
for i, (key, entry) in enumerate(raw_data.items()):
    # pro_ids = entry.get("pro_evidence_ids", [])
    # con_ids = entry.get("con_evidence_ids", [])
    # top_20_evidences = entry.get("top_20_evidences", [])
    # top_20_evidences_id = entry
    # merged_ids = list(set(pro_ids + con_ids))
    claim = example_to_claim[key]
    intent = entry["intent"]
    pro_claim = entry["pro_claim"]
    con_claim = entry["con_claim"]
    top_20_evidences = entry["top_20_evidences"]
    # Convert integer IDs to strings to match the dictionary keys
    evidence_full_text = [evidence_id_to_text[str(evidence_dict['evidence_id'])] for evidence_dict in top_20_evidences]
    # evidence_full_text = [f"[{idx+1}] {evidence_id_to_text[str(id)]}" for idx, id in enumerate(top_20_evidences)]
    # evidence_pro_text = [evidence_id_to_text[str(id)] for id in pro_ids]
    # evidence_con_text = [evidence_id_to_text[str(id)] for id in con_ids]
    merged_data[key] = {
        "claim": claim,
        "intent": intent,
        "pro_claim": pro_claim,
        "con_claim": con_claim,
        "top_20_evidences": top_20_evidences,
        "evidence_full_text": evidence_full_text
    }

with open("/home/yirui/mad/intent_enhanced_score_merged_evidence_ids_with_evi.json", "w") as f:
    json.dump(merged_data, f, indent=2)