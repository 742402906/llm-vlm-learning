import ollama


response = ollama.chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": "解释一下Transformer"
        }
    ]
)


print(response["message"]["content"])
