# Experiment 003: Temperature 参数影响测试

## 目的

理解 temperature 参数对模型输出随机性的影响。

## 设置

- 模型：Qwen3-8B（Ollama）
- Prompt：`介绍一下Transformer`（固定不变）
- 对比：`temperature=0` 与 `temperature=1`，各运行 2 次
- 脚本：`llm/inference/temperature_test.py`

## 现象记录

### temperature=0（两次运行对比）

两次输出高度一致：开头完全相同，正文仅个别词有微小差异（如 "LSTM、CNN" vs "LSTM、GRU"、"位置编码" vs "位置编码（Positional Encoding）"），篇幅几乎相同（88 行 vs 87 行）。

两次运行的开头逐字一致：

> Transformer 是一种革命性的深度学习模型架构，由 Google 团队于 2017 年提出（论文：Attention Is All You Need）。它通过自注意力机制和位置编码有效解决了传统序列模型（如 RNN、CNN）在处理长序列时的局限性……

### temperature=1（两次运行对比）

两次输出在结构、措辞、展开方式上明显不同：

- 第 1 次从"摒弃了传统 RNN 和 CNN 结构"的角度切入，且出现笔误 `2，017 年`（数字中混入中文逗号）
- 第 2 次从"通过引入自注意力机制解决传统模型局限性"的角度切入
- 章节标题相同（都是"1. 核心思想"），但标题下的内容组织完全不一样

## 结论

- temperature 控制采样随机性：**值越低**，模型越倾向选概率最高的词，输出越确定、可复现；**值越高**，低概率词被选中的机会变大，输出更多样，但稳定性下降（甚至出现笔误）。
- 经验法则：需要**稳定可复现**的场景（模型评测、结构化输出、批量数据处理）用低 temperature；需要**创意与多样性**的场景（写作、头脑风暴）用较高 temperature。

## 复现方式

```bash
conda activate llm-vlm-learning
python llm/inference/temperature_test.py
```
