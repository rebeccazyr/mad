import json
from collections import defaultdict

# Load JSON file containing a list of examples
with open("dataset/test.json", "r") as f:
    all_examples = json.load(f)

evidence_counts = [len(example["evidence"]) for example in all_examples]
evidence_counts_sorted = sorted(evidence_counts)
min_count = evidence_counts_sorted[0]
max_count = evidence_counts_sorted[-1]
mid = len(evidence_counts_sorted) // 2
if len(evidence_counts_sorted) % 2 == 1:
    median_count = evidence_counts_sorted[mid]
else:
    median_count = (evidence_counts_sorted[mid-1] + evidence_counts_sorted[mid]) / 2

print(f"Number of evidences per example: minimum {min_count}, maximum {max_count}, median {median_count}")

# Dictionary to track duplicate evidence sentences
evidence_map = defaultdict(list)

# Iterate through each evidence sentence and record its location
for example in all_examples:
    example_id = example["example_id"]
    for idx, sentence in enumerate(example["evidence"]):
        normalized = sentence.strip()
        evidence_map[normalized].append((example_id, idx))

# Report duplicates
duplicates = {k: v for k, v in evidence_map.items() if len(v) > 1}

print(f"\nTotal unique evidence sentences: {len(evidence_map)}")
print(f"Number of duplicated evidence sentences: {len(duplicates)}\n")

if duplicates:
    print("Duplicate evidence sentences and their locations:\n")
    for sentence, locations in duplicates.items():
        print(f"Sentence: \"{sentence}\"")
        print("Appears in:")
        for ex_id, idx in locations:
            print(f"  - example_id: {ex_id}, evidence_id: {idx}")
        print()
else:
    print("No duplicate evidence sentences found.")