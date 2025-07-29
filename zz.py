import json
import re

def remove_leading_numbers(data):
    """
    Remove leading [number] and optional space from each evidence text in 'evidence_full_text'.
    """
    for key, entry in data.items():
        if "evidence_full_text" in entry:
            entry["evidence_full_text"] = [
                re.sub(r"^\[\d+\]\s*", "", text) for text in entry["evidence_full_text"]
            ]
    return data

# 文件路径（你可以根据需要修改）
input_file = "/home/yirui/mad/bilin/evidence_bilingual_large_400_ready.json"
output_file = "/home/yirui/mad/bilin/evidence_bilingual_large_400_ready_noid.json"

# 读取原始 JSON
with open(input_file, "r", encoding="utf-8") as f:
    json_data = json.load(f)

# 处理数据
cleaned_data = remove_leading_numbers(json_data)

# 写入新文件
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

print(f"✅ Cleaned JSON saved to: {output_file}")