def compute_metrics(pred_ids, true_ids):
    pred_set = set(pred_ids)
    true_set = set(true_ids)
    fp = list(pred_set - true_set)
    true_list = list(true_set)

    return true_list, fp

def list_to_dict(items):
    return {item[0]: item[1] for item in items}

import json
with open("20_train_retrieved_evidence_map_bgebase.json") as f:
    result_dict = json.load(f)
with open("train/evidence_map.json") as f:
    gt_dict = json.load(f)

# Initialize output dictionary
output_dict = {}

for key in gt_dict:
    pred_ids = result_dict.get(key, [])
    true_ids = gt_dict[key]
    
    # Compute true positives and false positives
    true_list, fp = compute_metrics(pred_ids, true_ids)
    
    # Store results in the required format
    output_dict[key] = {
        "positive_ids": true_list,
        "negative_ids": fp
    }

with open("train_set.json", "w") as f:
    json.dump(output_dict, f, indent=4)