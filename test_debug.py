import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# 加载文件
json3 = load_json("/home/yirui/mad/intent_enhanced_retrieved_evidence.json")

# 读取ID列表
with open("id_list.txt", "r") as f:
    id_list = [line.strip() for line in f if line.strip()]

print(f"JSON3 keys type: {type(list(json3.keys())[0])}")
print(f"First few keys: {list(json3.keys())[:5]}")
print(f"ID list type: {type(id_list[0])}")
print(f"First few IDs: {id_list[:5]}")

# 测试几个ID
for i, id_ in enumerate(id_list[:3]):
    print(f"\nTesting ID: {id_}")
    print(f"ID type: {type(id_)}")
    print(f"ID in json3: {id_ in json3}")
    print(f"json3.get result: {json3.get(id_, 'Not Found')}")
    if i >= 2:
        break 