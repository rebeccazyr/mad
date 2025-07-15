import json
import re

# Load the input JSON file
with open("/home/yirui/mad/dataset/test.json", "r") as f:
    data_list = json.load(f)

# Result dictionary: {example_id: veracity}
id_to_veracity = {}

# Iterate through the first 200 entries
for entry in data_list[:200]:
    example_id = str(entry.get("example_id"))
    veracity = entry.get("veracity", "").upper()  # Normalize to uppercase: 'half-true' → 'HALF-TRUE'
    id_to_veracity[example_id] = veracity


# Optionally, write the result to an output file
with open("/home/yirui/mad/transformed_GT_200.json", "w") as f:
    json.dump(id_to_veracity, f, indent=2)