import json
from collections import defaultdict

# File paths (replace with your actual file names if different)
groundtruth_file = "./data/transformed_GT_200.json"
prediction_files = [
    "./data/transformed_answer_map_retrived_evidence_single_200.json",
    "./data/transformed_answer_map_retrived_evidence_multi_200.json",
    "./data/transformed_answer_map_single_200.json",
    "./data/transformed_answer_map_multi_200.json"
]

def calculate_f1_score(precision, recall):
    """Calculate F1 score from precision and recall"""
    if precision + recall == 0:
        return 0.0
    return 2 * (precision * recall) / (precision + recall)

def calculate_class_metrics(y_true, y_pred, class_label):
    """Calculate precision, recall, and F1 for a specific class"""
    tp = 0  # True positives
    fp = 0  # False positives
    fn = 0  # False negatives
    
    for true_val, pred_val in zip(y_true, y_pred):
        if true_val == class_label and pred_val == class_label:
            tp += 1
        elif true_val != class_label and pred_val == class_label:
            fp += 1
        elif true_val == class_label and pred_val != class_label:
            fn += 1
    
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = calculate_f1_score(precision, recall)
    
    return precision, recall, f1

# Load ground truth
with open(groundtruth_file, "r") as f:
    groundtruth = json.load(f)

# Compare each prediction file with ground truth
for pred_file in prediction_files:
    with open(pred_file, "r") as pf:
        prediction = json.load(pf)

    total = 0
    correct = 0
    half_true = 0
    half_true_correct = 0
    false = 0
    false_correct = 0
    true = 0
    true_correct = 0
    
    # Lists to store true and predicted labels for F1 calculation
    y_true = []
    y_pred = []

    for key in groundtruth:
        if key in prediction:
            total += 1
            y_true.append(groundtruth[key])
            y_pred.append(prediction[key])
            
            if groundtruth[key] == prediction[key]:
                correct += 1
            if groundtruth[key] == "HALF-TRUE":
                half_true += 1
                if groundtruth[key] == prediction[key]:
                    half_true_correct += 1
            if groundtruth[key] == "FALSE":
                false += 1
                if groundtruth[key] == prediction[key]:
                    false_correct += 1
            if groundtruth[key] == "TRUE":
                true += 1
                if groundtruth[key] == prediction[key]:
                    true_correct += 1

    # Calculate accuracy metrics
    accuracy = correct / total if total > 0 else 0.0
    half_true_accuracy = half_true_correct / half_true if half_true > 0 else 0.0
    false_accuracy = false_correct / false if false > 0 else 0.0
    true_accuracy = true_correct / true if true > 0 else 0.0
    
    # Calculate F1 scores for each class
    true_precision, true_recall, true_f1 = calculate_class_metrics(y_true, y_pred, "TRUE")
    half_true_precision, half_true_recall, half_true_f1 = calculate_class_metrics(y_true, y_pred, "HALF-TRUE")
    false_precision, false_recall, false_f1 = calculate_class_metrics(y_true, y_pred, "FALSE")
    
    # Calculate Macro-F1 (average of all class F1 scores)
    macro_f1 = (true_f1 + half_true_f1 + false_f1) / 3
    
    print(f"File: {pred_file}")
    print(f"  Total examples compared: {total}")
    print(f"  Correct predictions: {correct}")
    print(f"  Overall Accuracy: {accuracy:.2%}")
    print()
    
    # Class-wise accuracy
    print(f"  Class-wise Accuracy:")
    print(f"    TRUE: {true_accuracy:.2%} ({true_correct}/{true})")
    print(f"    HALF-TRUE: {half_true_accuracy:.2%} ({half_true_correct}/{half_true})")
    print(f"    FALSE: {false_accuracy:.2%} ({false_correct}/{false})")
    print()
    
    # F1 scores
    print(f"  F1 Scores:")
    print(f"    TRUE - Precision: {true_precision:.2%}, Recall: {true_recall:.2%}, F1: {true_f1:.2%}")
    print(f"    HALF-TRUE - Precision: {half_true_precision:.2%}, Recall: {half_true_recall:.2%}, F1: {half_true_f1:.2%}")
    print(f"    FALSE - Precision: {false_precision:.2%}, Recall: {false_recall:.2%}, F1: {false_f1:.2%}")
    print(f"    Macro-F1: {macro_f1:.2%}")
    print("-" * 80)