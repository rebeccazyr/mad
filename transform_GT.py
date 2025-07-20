import json
import re

# Load the input JSON file
with open("/home/yirui/mad/chroma/test.json", "r") as f:
    data_list = json.load(f)

# Result dictionary: {example_id: veracity}
id_to_veracity = {}
ids = []
# Iterate through the first 200 entries
# for entry in data_list[:200]:
for entry in data_list:
    example_id = str(entry.get("example_id"))
    ids.append(example_id)
    veracity = entry.get("veracity", "").upper()  # Normalize to uppercase: 'half-true' → 'HALF-TRUE'
    id_to_veracity[example_id] = veracity


# Optionally, write the result to an output file
with open("/home/yirui/mad/train/data/GT_test_all.json", "w") as f:
    json.dump(id_to_veracity, f, indent=2)
# with open("/home/yirui/mad/ids_400.json", "w") as f:
#     json.dump(ids, f, indent=2)