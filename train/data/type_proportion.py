import json
from collections import Counter

# Load the JSON file
with open("/home/yirui/mad/data/transformed_GT_200.json", "r") as f:
    data = json.load(f)

# Count occurrences of each label
label_counts = Counter(data.values())

# Total number of entries
total = sum(label_counts.values())

# Print count and percentage for each label
for label, count in label_counts.items():
    percentage = (count / total) * 100
    print(f"{label}: {count} ({percentage:.2f}%)")