import json
import re

# Load the input JSON file
with open("/home/yirui/mad/bilin/400_answer_map_bge_con_pro_noid_multi_3p.json", "r") as f:
    data = json.load(f)

# Dictionary to store the mapping from example ID to verdict
id_to_verdict = {}

# Iterate through the first 200 examples in the JSON
for idx, (example_id, content) in enumerate(data.items()):
    
    final_verdict = content.get("final_verdict", "")
    
    # Use regex to extract the verdict: TRUE, FALSE, or HALF-TRUE
    # Support both [VERDICT]: and VERDICT: formats, with optional newlines and whitespace
    match = re.search(r'\[?VERDICT\]:\s*(TRUE|FALSE|HALF-TRUE)', final_verdict, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    
    # If the first pattern doesn't match, try a more flexible pattern
    if not match:
        match = re.search(r'VERDICT\s*:\s*(TRUE|FALSE|HALF-TRUE)', final_verdict, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    
    if match:
        id_to_verdict[example_id] = match.group(1)
    else:
        # If no standard format found, search for the keywords in the text
        keyword_match = re.search(r'\b(TRUE|FALSE|HALF-TRUE)\b', final_verdict, re.IGNORECASE)
        if keyword_match:
            id_to_verdict[example_id] = keyword_match.group(1)
        else:
            id_to_verdict[example_id] = "UNKNOWN"  # Fallback if no keywords found

# Optionally, write the result to an output file
with open("/home/yirui/mad/bilin/trans/400_answer_map_bge_con_pro_noid_multi_3p.json", "w") as f:
    json.dump(id_to_verdict, f, indent=2)