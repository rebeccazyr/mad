import json

with open("/home/yirui/mad/data/retrived_evidence_query.json", "r") as f:
    all_examples = json.load(f)

with open("/home/yirui/mad/ids_400.json", "r") as f:
    ids = json.load(f)

evidence_list = []

for example in all_examples:
    example_id = example["example_id"]
    if example_id in ids:
        evidence_list.append(example)

with open("/home/yirui/mad/data/retrived_evidence_query_400.json", "w") as f:
    json.dump(evidence_list, f, indent=2)