# app/model.py

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# モデルのロード（初回は数分かかる）
model_id = "google/gemma-2b-it"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

# 推論用パイプライン
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# 要約関数
def summarize_text(text: str) -> str:
    prompt = f"以下の文章を日本語で要約してください。\n\n{text}\n\n要約："
    output = pipe(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
    return output[0]["generated_text"].split("要約：")[-1].strip()
