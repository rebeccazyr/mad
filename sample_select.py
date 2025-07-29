import json
import pandas as pd

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def find_disagreements(json1, json2, json3, json4):
    # Get common keys
    common_keys = set(json1.keys()) & set(json2.keys()) & set(json3.keys()) & set(json4.keys())
    
    rows = []
    for key in sorted(common_keys, key=int):
        v1, v2, v3, v4 = json1[key], json2[key], json3[key], json4[key]
        if len(set([str(v1), str(v2), str(v3), str(v4)])) > 1:  # convert to str to avoid unhashable types
            rows.append({
                "ID": key,
                "GT": v1,
                "Retrived_Evidence": v2,
                "Full_Evidence": v3,
                "Intent_Enhanced": v4
            })
    return pd.DataFrame(rows)

if __name__ == "__main__":
    # Replace with your actual paths
    file1 = "/home/yirui/mad/transformed_GT_400.json"
    file2 = "/home/yirui/mad/400_transformed_answer_map_retrived_evidence_single.json"
    file3 = "/home/yirui/mad/400_transformed_answer_map_single.json"
    file4 = "/home/yirui/mad/intent_enhanced/tras/400_transformed_answer_map_single.json"

    json1 = load_json(file1)
    json2 = load_json(file2)
    json3 = load_json(file3)
    json4 = load_json(file4)

    df = find_disagreements(json1, json2, json3, json4)

    # Write to Excel
    df.to_excel("disagreements.xlsx", sheet_name="Disagreement Analysis", index=False)
    print("Saved to disagreements.xlsx")