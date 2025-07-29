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

    common_keys = [key for key in gt_dict.keys() if key in result_dict]
    print(len(common_keys))
    for key in common_keys:
        pred_ids = result_dict[key]
        true_ids = gt_dict[key]
        
        precision, recall, f1 = compute_metrics(pred_ids, true_ids)
        # print(f"Key: {key}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}")
        all_precisions.append(precision)
        all_recalls.append(recall)
        all_f1s.append(f1)

    macro_precision = sum(all_precisions) / len(all_precisions) if all_precisions else 0.0
    macro_recall = sum(all_recalls) / len(all_recalls) if all_recalls else 0.0
    macro_f1 = sum(all_f1s) / len(all_f1s) if all_f1s else 0.0

    return macro_precision, macro_recall, macro_f1

import json
with open("/home/yirui/mad/intent_enhanced_bilingual_large_con_only_400_top20_by_score_merged_ids.json") as f:
    result_dict = json.load(f)
with open("/home/yirui/mad/chroma/evidence_map.json") as f:
    gt_dict = json.load(f)

macro_precision, macro_recall, macro_f1 = evaluate_all(result_dict, gt_dict)
print(f"Macro Precision: {macro_precision:.4f}")
print(f"Macro Recall:    {macro_recall:.4f}")
print(f"Macro F1-score:  {macro_f1:.4f}")