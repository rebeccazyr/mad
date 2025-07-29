import json
import pandas as pd

with open("id_list.txt", "r") as f:
    id_list = [line.strip() for line in f if line.strip()]

with open("/home/yirui/mad/intent_enhanced/400_answer_map_single.json", "r") as f:
    intent = json.load(f)

with open("/home/yirui/mad/400_answer_map_retrived_evidence_single.json", "r") as f:
    retrieved = json.load(f)

with open("/home/yirui/mad/400_answer_map_single.json", "r") as f:
    single = json.load(f)



# 构建要保存的数据行
rows = []
for id_ in id_list:
    intent_evi = intent.get(id_, "❌ Not Found")
    retrieved_evi = retrieved.get(id_, "❌ Not Found")
    single_evi = single.get(id_, "❌ Not Found")
    rows.append({"ID": id_, "Full_Evidence": single_evi, "Retrieved_Evidence": retrieved_evi, "Intent_Enhanced": intent_evi})

# 创建 DataFrame 并保存为 Excel 文件
df = pd.DataFrame(rows)
df.to_excel("selected_sentences_1.xlsx", index=False)

print("✅ Saved to selected_sentences.xlsx")
