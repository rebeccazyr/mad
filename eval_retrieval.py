def compute_metrics(pred_ids, true_ids):
    pred_set = set(pred_ids)
    true_set = set(true_ids)
    
    tp = len(pred_set & true_set)
    fp = len(pred_set - true_set)
    fn = len(true_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return precision, recall, f1

def evaluate_all(result_dict, gt_dict):
    all_precisions = []
    all_recalls = []
    all_f1s = []

    for key in gt_dict:
        pred_ids = result_dict.get(key, [])
        true_ids = gt_dict[key]
        
        precision, recall, f1 = compute_metrics(pred_ids, true_ids)
        all_precisions.append(precision)
        all_recalls.append(recall)
        all_f1s.append(f1)

    macro_precision = sum(all_precisions) / len(all_precisions) if all_precisions else 0.0
    macro_recall = sum(all_recalls) / len(all_recalls) if all_recalls else 0.0
    macro_f1 = sum(all_f1s) / len(all_f1s) if all_f1s else 0.0

    return macro_precision, macro_recall, macro_f1

import json
with open("50_retrieved_evidence_map_bgebase.json") as f:
    result_dict = json.load(f)
with open("evidence_map.json") as f:
    gt_dict = json.load(f)

macro_precision, macro_recall, macro_f1 = evaluate_all(result_dict, gt_dict)
print(f"Macro Precision: {macro_precision:.4f}")
print(f"Macro Recall:    {macro_recall:.4f}")
print(f"Macro F1-score:  {macro_f1:.4f}")