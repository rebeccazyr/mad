import json

# File paths (replace with your actual file names if different)
groundtruth_file = "transformed_GT_200.json"
prediction_files = [
    "transformed_answer_map_retrived_evidence_multi_200.json",
    "transformed_answer_map_retrived_evidence_single_200.json",
    "transformed_answer_map_single_200.json",
    "transformed_answer_map_multi_200.json"
]

# Load ground truth
with open(groundtruth_file, "r") as f:
    groundtruth = json.load(f)

# Compare each prediction file with ground truth
for pred_file in prediction_files:
    with open(pred_file, "r") as pf:
        prediction = json.load(pf)

    total = 0
    correct = 0

    for key in groundtruth:
        if key in prediction:
            total += 1
            if groundtruth[key] == prediction[key]:
                correct += 1

    accuracy = correct / total if total > 0 else 0.0
    print(f"File: {pred_file}")
    print(f"  Total examples compared: {total}")
    print(f"  Correct predictions: {correct}")
    print(f"  Accuracy: {accuracy:.2%}")
    print()