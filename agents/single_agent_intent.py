from model.loader import load_model
from prompts.templates import system_prompt_fact_checker, user_prompt_single_agent_intent, user_prompt_intent_inference, get_system_prompt

# Load model and tokenizer once
tokenizer, model = load_model()

def infer_intent(claim):
    return run_model(get_system_prompt("fact_checker"), user_prompt_intent_inference(claim))


def final_verdict(claim, evidence, intent):
    prompt = user_prompt_single_agent_intent(claim, evidence, intent)
    return run_model(get_system_prompt("fact_checker"), prompt)


# === Shared model runner ===
def run_model(system_prompt: str, user_prompt: str):
    full_prompt = f"<|begin_of_text|><|system|>\n{system_prompt}\n<|user|>\n{user_prompt}<|assistant|>\n"
    inputs = tokenizer(full_prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        do_sample=False,
        temperature=0.7,
        eos_token_id=tokenizer.eos_token_id
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("<|assistant|>")[-1].strip()