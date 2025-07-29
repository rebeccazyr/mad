from chroma.chroma import ChromaClient
from model.loader import load_model
from prompts.templates import (
    get_system_prompt,
    user_prompt_intent_inference,
    user_prompt_generate_con_queries,
    user_prompt_generate_pro_queries,
    user_prompt_extract_terms
)
import json
from tqdm import tqdm
import os
import re

# === Load model for all agents ===
tokenizer, model = load_model()

# === Shared model runner ===
def run_model(system_prompt: str, user_prompt: str, max_tokens: int = 300):
    full_prompt = f"<|begin_of_text|><|system|>\n{system_prompt}\n<|user|>\n{user_prompt}<|assistant|>\n"
    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        do_sample=False,
        temperature=0.7,
        eos_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("<|assistant|>")[-1].strip()

# === Sub-functions ===
def infer_intent(claim):
    return run_model(get_system_prompt("fact_checker"), user_prompt_intent_inference(claim), max_tokens=150)

def extract_terms(claim):
    return run_model(get_system_prompt("fact_checker"), user_prompt_extract_terms(claim), max_tokens=150)

def generate_pro_queries(claim, intent, keywords):
    return run_model(get_system_prompt("debater"), user_prompt_generate_pro_queries(claim, intent, keywords))

def generate_con_queries(claim, intent, keywords):
    return run_model(get_system_prompt("debater"), user_prompt_generate_con_queries(claim, intent, keywords))

def extract_clean_json(text: str, field: str):
    match = re.search(r'{\s*"' + field + r'"\s*:\s*\[.*?\]\s*}', text, re.DOTALL)
    if not match:
        raise ValueError("Failed to extract valid JSON for field: " + field)
    return json.loads(match.group(0))

def intent_enhanced_reformulation(claim: str):
    print(f"\n[CLAIM] {claim}")
    intent = infer_intent(claim)
    print(f"[INTENT] {intent}")

    keywords = extract_terms(claim)
    print(f"[KEYWORDS] {keywords}")

    pro_raw = generate_pro_queries(claim, intent, keywords)
    print(f"[PRO JSON RAW] {pro_raw}")
    pro_queries = extract_clean_json(pro_raw, "pro_statements").get("pro_statements", [])

    con_raw = generate_con_queries(claim, intent, keywords)
    print(f"[CON JSON RAW] {con_raw}")
    con_queries = extract_clean_json(con_raw, "con_statements").get("con_statements", [])

    return {
        "intent": intent,
        "keywords": keywords,
        "pro_queries": pro_queries,
        "con_queries": con_queries
    }
