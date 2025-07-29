from model.loader import load_model
from prompts.templates4 import (
    get_system_prompt,
    user_prompt_opening_true,
    user_prompt_opening_halftrue,
    user_prompt_opening_false,
    user_prompt_rebuttal_true,
    user_prompt_rebuttal_halftrue,
    user_prompt_rebuttal_false,
    user_prompt_closing_true,
    user_prompt_closing_halftrue,
    user_prompt_closing_false,
    user_prompt_judge_full_triagent
)

# Load model once for all agents
tokenizer, model = load_model()


# === TRUE Agent ===
def opening_true(claim, evidence):
    prompt = user_prompt_opening_true(claim, evidence)
    return run_model(get_system_prompt("true_agent"), prompt)

def rebuttal_true(claim, evidence, halftrue_argument, false_argument):
    prompt = user_prompt_rebuttal_true(claim, evidence, halftrue_argument, false_argument)
    return run_model(get_system_prompt("true_agent"), prompt)

def closing_true(claim, evidence):
    prompt = user_prompt_closing_true(claim, evidence)
    return run_model(get_system_prompt("true_agent"), prompt)


# === HALF-TRUE Agent ===
def opening_halftrue(claim, evidence):
    prompt = user_prompt_opening_halftrue(claim, evidence)
    return run_model(get_system_prompt("halftrue_agent"), prompt)

def rebuttal_halftrue(claim, evidence, true_argument, false_argument):
    prompt = user_prompt_rebuttal_halftrue(claim, evidence, true_argument, false_argument)
    return run_model(get_system_prompt("halftrue_agent"), prompt)

def closing_halftrue(claim, evidence):
    prompt = user_prompt_closing_halftrue(claim, evidence)
    return run_model(get_system_prompt("halftrue_agent"), prompt)


# === FALSE Agent ===
def opening_false(claim, evidence):
    prompt = user_prompt_opening_false(claim, evidence)
    return run_model(get_system_prompt("false_agent"), prompt)

def rebuttal_false(claim, evidence, true_argument, halftrue_argument):
    prompt = user_prompt_rebuttal_false(claim, evidence, true_argument, halftrue_argument)
    return run_model(get_system_prompt("false_agent"), prompt)

def closing_false(claim, evidence):
    prompt = user_prompt_closing_false(claim, evidence)
    return run_model(get_system_prompt("false_agent"), prompt)


# === JUDGE Agent ===
def judge_final_verdict(
    claim, evidence,
    true_open, halftrue_open, false_open,
    true_rebut, halftrue_rebut, false_rebut,
    true_close, halftrue_close, false_close
):
    prompt = user_prompt_judge_full_triagent(
        claim, evidence,
        true_open, halftrue_open, false_open,
        true_rebut, halftrue_rebut, false_rebut,
        true_close, halftrue_close, false_close
    )
    return run_model(get_system_prompt("judge"), prompt, max_tokens=400)


# === Shared Model Runner ===
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