import json

with open("/home/yirui/mad/data/20_retrieved_evidence_map_bgebase.json", "r") as f:
    all_examples = json.load(f)

with open("/home/yirui/mad/chroma/example_to_claim.json", "r") as f:
    example_to_claim = json.load(f)

with open("/home/yirui/mad/chroma/evidence_id_to_text.json", "r") as f:
    evidence_id_to_text = json.load(f)

all_examples_list = []

for example_id, evidence_ids in all_examples.items():
    claim = example_to_claim[example_id]
    evidence_list = [evidence_id_to_text[str(evidence_id)] for evidence_id in evidence_ids]
    example = {
        "example_id": example_id,
        "claim": claim,
        "evidence": evidence_list
    }
    all_examples_list.append(example)

with open("/home/yirui/mad/data/retrived_evidence_query.json", "w") as f:
    json.dump(all_examples_list, f, indent=2)
