import json

# Load input JSON
with open("/home/yirui/mad/intent_enhanced_con_only_bilingual_large_400_top20_by_score.json", "r") as f:
    raw_data = json.load(f)

filtered_data = {}

for i, (key, entry) in enumerate(raw_data.items()):
    # pro_ids = entry.get("pro_evidence_ids", [])
    # con_ids = entry.get("con_evidence_ids", [])
    # merged_ids = list(set(pro_ids + con_ids))
    merged_ids = entry.get("top_20_evidences", [])
    filtered_data[key] = merged_ids
    print(i)

# Save output
with open("intent_enhanced_bilingual_large_con_only_400_top20_by_score_merged_ids.json", "w") as f:
    json.dump(filtered_data, f, indent=2)