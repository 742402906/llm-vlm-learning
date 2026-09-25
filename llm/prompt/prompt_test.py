"""第一个 AI 测试框架雏形。

流程：读取 prompt -> 调用 Qwen3 -> 保存结果 -> 生成实验报告

指标：
- completeness（完整性）0/1/2：是否覆盖 Encoder / Decoder / Attention / Position Encoding
  0=没有回答 1=简单提到（覆盖部分概念） 2=完整解释（4 个概念全覆盖）
- accuracy（准确性）：人工检查，报告里留了检查位
- instruction_following（指令遵循）0/1/2：是否按 expected_sections 给出章节；
  prompt 没有章节要求时为 N/A
"""

import json
import re
from datetime import datetime
from pathlib import Path

import ollama

MODEL = "qwen3:8b"
HERE = Path(__file__).resolve().parent
RESULTS_DIR = HERE / "results"

CONCEPT_KEYWORDS = {
    "Encoder": ("encoder", "编码器"),
    "Decoder": ("decoder", "解码器"),
    "Attention": ("attention", "注意力"),
    "Position Encoding": ("position", "位置编码"),
}


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


def score_completeness(text: str) -> dict:
    found = {
        concept: any(kw in text.lower() for kw in keywords)
        for concept, keywords in CONCEPT_KEYWORDS.items()
    }
    covered = sum(found.values())
    score = 0 if covered == 0 else (1 if covered < len(CONCEPT_KEYWORDS) else 2)
    return {"score": score, "covered": found}


def score_instruction_following(text: str, expected_sections):
    if not expected_sections:
        return None
    numbers = set()
    for line in text.splitlines():
        m = re.match(r"\s*#{0,6}\s*(\d+)\.", line)
        if m:
            numbers.add(int(m.group(1)))
    score = 2 if len(numbers) >= expected_sections else (1 if numbers else 0)
    return {"score": score, "sections_found": sorted(numbers), "expected": expected_sections}


def build_report(timestamp: str, rows: list) -> str:
    lines = [
        f"# Prompt 评测报告 {timestamp}",
        "",
        f"模型：{MODEL}",
        "",
        "| Prompt | Completeness | Instruction Following | Accuracy |",
        "|---|---|---|---|",
    ]
    for r in rows:
        i = "N/A" if r["instruction_following"] is None else r["instruction_following"]["score"]
        lines.append(f"| {r['name']} | {r['completeness']['score']} | {i} | 人工待评 |")
    lines.append("")
    for r in rows:
        covered = ", ".join(c for c, ok in r["completeness"]["covered"].items() if ok) or "无"
        lines += [
            f"## {r['name']}",
            "",
            f"Completeness 覆盖概念：{covered}",
            "",
            "Output:",
            "",
            "```text",
            r["output"],
            "```",
            "",
        ]
    return "\n".join(lines)


def main() -> None:
    prompts = json.loads((HERE / "prompts.json").read_text(encoding="utf-8"))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    RESULTS_DIR.mkdir(exist_ok=True)

    rows = []
    for item in prompts:
        print(f"[run] {item['name']} ...")
        output = ask(item["prompt"])
        rows.append(
            {
                "name": item["name"],
                "prompt": item["prompt"],
                "output": output,
                "completeness": score_completeness(output),
                "instruction_following": score_instruction_following(
                    output, item.get("expected_sections")
                ),
                "accuracy": "manual",
            }
        )

    results_path = RESULTS_DIR / f"results_{timestamp}.json"
    results_path.write_text(
        json.dumps(
            {"timestamp": timestamp, "model": MODEL, "results": rows},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    report_path = RESULTS_DIR / f"report_{timestamp}.md"
    report_path.write_text(build_report(timestamp, rows), encoding="utf-8")

    print(f"\n[done] results -> results/{results_path.name}")
    print(f"[done] report  -> results/{report_path.name}\n")
    for r in rows:
        i = "N/A" if r["instruction_following"] is None else r["instruction_following"]["score"]
        print(f"{r['name']}: completeness={r['completeness']['score']}  instruction_following={i}  accuracy=人工待评")


if __name__ == "__main__":
    main()
