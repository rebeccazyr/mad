def compute_metrics(pred_ids, true_ids):
    pred_set = set(pred_ids)
    true_set = set(true_ids)
    tp = list(pred_set & true_set)
    fp = list(pred_set - true_set)

    return tp, fp

def list_to_dict(items):
    return {item[0]: item[1] for item in items}

import json
with open("20_train_retrieved_evidence_map_bgebase.json") as f:
    result_dict = json.load(f)
with open("train/evidence_map.json") as f:
    gt_dict = json.load(f)
true = []
false = []
for key in gt_dict:
        pred_ids = result_dict.get(key, [])
        true_ids = gt_dict[key]
        score_list = list_to_dict(score_dict[key])
        tp, fp = compute_metrics(pred_ids, true_ids)
with open("train_set.json", "w") as f:
    json.dump([sorted(true), sorted(false)], f, indent=4)