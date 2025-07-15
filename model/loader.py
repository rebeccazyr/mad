from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def load_model(model_path="./llama3-8b-instruct"):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        device_map="auto",
        torch_dtype=torch.float16
    )
    return tokenizer, model