import ollama

MODEL = "qwen3:8b"

CASES = [
    (
        "Case 1: Zero-shot",
        "解释Transformer",
    ),
    (
        "Case 2: 角色 Prompt",
        "你是一名人工智能领域专家。\n\n"
        "请解释Transformer。\n\n"
        "要求：\n"
        "1. 面向AI初学者\n"
        "2. 使用简单语言\n"
        "3. 给出实际例子",
    ),
    (
        "Case 3: 结构化 Prompt",
        "请按照以下结构解释Transformer：\n\n"
        "# 1. Transformer解决什么问题\n\n"
        "# 2. 核心组成\n\n"
        "# 3. Attention机制\n\n"
        "# 4. 一个生活中的例子\n\n"
        "# 5. 总结",
    ),
]


def ask(prompt: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    return response["message"]["content"]


def main() -> None:
    for title, prompt in CASES:
        print(f"\n{'=' * 60}")
        print(title)
        print("=" * 60)
        print(ask(prompt))


if __name__ == "__main__":
    main()
