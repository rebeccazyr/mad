import json

# 加载 JSON 数据
with open("/home/yirui/mad/bilin/400_answer_map_bge_con_pro_noid_multi_role.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 提取一对一的角色
role_pairs = []

for example in data.values():
    support = example.get("support_role")
    oppose = example.get("oppose_role")
    if support and oppose:
        role_pairs.append((support.strip(), oppose.strip()))

# 打印所有一对一的角色组合
for idx, (support, oppose) in enumerate(role_pairs, 1):
    print(f"{idx}. SUPPORTING_ROLE: {support}\n   OPPOSING_ROLE: {oppose}\n")

# （可选）保存到文件
with open("role_pairs.txt", "w", encoding="utf-8") as out:
    for support, oppose in role_pairs:
        out.write(f"SUPPORTING_ROLE: {support}\nOPPOSING_ROLE: {oppose}\n\n")