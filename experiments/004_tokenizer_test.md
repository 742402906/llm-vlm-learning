# Experiment 004: Tokenizer 与 Token 理解

## 目的

理解 `文本 → Tokenizer → Token → 模型` 流水线的第一步：文本如何被切分成 token。

## 设置

- Tokenizer：`Qwen/Qwen3-8B`（transformers 的 AutoTokenizer 加载，只下载 tokenizer 文件，不下载模型权重）
- 输入文本：`你好, Transformer`
- 脚本：`llm/inference/tokenizer_test.py`

## 结果

```text
['ä½łå¥½', ',', 'ĠTransformer']
[108386, 11, 62379]
共 3 个 token
```

## 观察与解释

1. **`你好` 是 1 个 token**（ID 108386），但显示成 `ä½łå¥½` 的样子——这是 byte-level BPE 的显示方式：tokenizer 把文本的 UTF-8 字节逐个映射成可打印字符再合并，`你好` 的 6 个字节显示为这 4 个字符。token 本身没有问题，只是展示层的样子，模型内部使用的是 ID。
2. **`,` 单独占 1 个 token**（ID 11）——标点也是 token。
3. **` Transformer` 是 1 个 token**（ID 62379），开头的 `Ġ` 代表空格（字节 0x20 的映射字符）——**空格被计入 token**，这是英文单词前带 `Ġ` 的原因。
4. 模型看到的从来不是"字"或"词"，而是 **token ID 序列**：`[108386, 11, 62379]`。中文常用词、英文常见词通常是 1 个 token；生僻词会被拆成多个子词（subword）。

## 环境备注

- `transformers 5.17.0`，只装了 tokenizer 部分，没有 PyTorch（运行时的警告可忽略，不影响 tokenizer 功能）
- 下载 tokenizer 走了国内镜像 `HF_ENDPOINT=https://hf-mirror.com`（直连 huggingface.co 不通）

## 复现方式

```bash
conda activate llm-vlm-learning
HF_ENDPOINT=https://hf-mirror.com python llm/inference/tokenizer_test.py
```
