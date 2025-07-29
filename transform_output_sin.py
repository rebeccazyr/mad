import json
import re

# Load the input JSON file
with open("/home/yirui/mad/bilin/400_answer_map_intent_enhanced_single_sep.json", "r") as f:
    data = json.load(f)

# Dictionary to store the mapping from example ID to verdict
id_to_verdict = {}

# Iterate through the first 200 examples in the JSON
for idx, (example_id, verdict_list) in enumerate(data.items()):
    
    # Take the first (and only) string from the list
    verdict_text = verdict_list[0] if verdict_list else ""


    # Use regex to extract the verdict: TRUE, FALSE, or HALF-TRUE
    # Handle various formats: [VERDICT]:, **VERDICT:**, VERDICT:, etc.
    match = re.search(r'\[?VERDICT\]:\s*(TRUE|FALSE|HALF-TRUE)', verdict_text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    
    # If the first pattern doesn't match, try a more flexible pattern for **VERDICT:**
    if not match:
        match = re.search(r'\*\*VERDICT\*\*:.*?(TRUE|FALSE|HALF-TRUE)', verdict_text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    
    # If still no match, try the most flexible pattern
    if not match:
        match = re.search(r'VERDICT\s*:\s*(TRUE|FALSE|HALF-TRUE)', verdict_text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    
    # If still no match, try an even more flexible pattern
    if not match:
        match = re.search(r'VERDICT.*?(TRUE|FALSE|HALF-TRUE)', verdict_text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    
    if match:
        id_to_verdict[example_id] = match.group(1)
    else:
        id_to_verdict[example_id] = "UNKNOWN"
        
# Optionally, write the result to an output file
with open("/home/yirui/mad/bilin/trans/400_answer_map_intent_cot_single.json", "w") as f:
    json.dump(id_to_verdict, f, indent=2)