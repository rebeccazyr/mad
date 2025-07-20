import json
import random

with open("/home/yirui/mad/dataset/test.json", "r") as f:
    data = json.load(f)

sampled_data = random.sample(data, 400)

with open("/home/yirui/mad/dataset/test_400.json", "w") as f:
    json.dump(sampled_data, f, indent=2)