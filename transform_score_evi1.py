import json

# Load input JSON
with open("/home/yirui/mad/intent_enhanced_400_retrieved_simple_20_ranked_each_evidence_with_keywords_points_score.json", "r") as f:
    raw_data = json.load(f)

filtered_data = {}

for i, (key, entry) in enumerate(raw_data.items()):
    # pro_ids = entry.get("pro_evidence_ids", [])
    # con_ids = entry.get("con_evidence_ids", [])
    # merged_ids = list(set(pro_ids + con_ids))
    merged_ids = entry.get("top_20_evidences", [])
    print(merged_ids)
    filtered_data[key] = merged_ids

# Save output
with open("intent_enhanced_400_retrieved_simple_20_ranked_each_evidence_with_keywords_points_score_merged_ids.json", "w") as f:
    json.dump(filtered_data, f, indent=2)