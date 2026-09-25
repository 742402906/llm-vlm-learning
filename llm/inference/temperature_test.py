import ollama

PROMPT = "介绍一下Transformer"


def ask(temperature: float) -> str:
    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": PROMPT,
            }
        ],
        options={"temperature": temperature},
    )
    return response["message"]["content"]


def main() -> None:
    for temp in (0, 1):
        for run in (1, 2):
            print(f"\n{'=' * 60}")
            print(f"temperature={temp}  第 {run} 次运行")
            print("=" * 60)
            print(ask(temp))


if __name__ == "__main__":
    main()
