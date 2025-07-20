import json
import re

# Load the input JSON file
with open("/home/yirui/mad/400_answer_map_multi.json", "r") as f:
    data = json.load(f)

# Dictionary to store the mapping from example ID to verdict
id_to_verdict = {}

# Iterate through the first 200 examples in the JSON
for idx, (example_id, content) in enumerate(data.items()):
    
    final_verdict = content.get("final_verdict", "")
    
    # Use regex to extract the verdict: TRUE, FALSE, or HALF-TRUE
    match = re.search(r'VERDICT:\s*(TRUE|FALSE|HALF-TRUE)', final_verdict)
    
    if match:
        id_to_verdict[example_id] = match.group(1)
    else:
        id_to_verdict[example_id] = "UNKNOWN"  # Fallback if verdict not found

# Optionally, write the result to an output file
with open("/home/yirui/mad/400_transformed_answer_map_multi.json", "w") as f:
    json.dump(id_to_verdict, f, indent=2)