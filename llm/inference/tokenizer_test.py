from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen3-8B"
)

text = "你好, Transformer"

tokens = tokenizer.tokenize(text)

print(tokens)

# 扩展观察：每个 token 对应的 ID，以及总数
token_ids = tokenizer.convert_tokens_to_ids(tokens)
print(token_ids)
print(f"共 {len(tokens)} 个 token")
