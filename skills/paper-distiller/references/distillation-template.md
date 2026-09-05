# Distillation Template / 论文蒸馏模板

Use this as the internal structure for the answer and the data passed to `visualize`.

## 0. Source Card / 来源卡片

- Title / 标题:
- Authors / 作者:
- Source / 来源:
- Date / 日期:
- Input type / 输入类型:
- Mode / 模式:
- Source caveats / 来源限制:

## 1. One-Sentence Thesis / 一句话主旨

Chinese:
English:

Make this understandable to a smart non-specialist. Avoid jargon unless the paper cannot be identified without it.

## 2. Why This Paper Exists / 为什么需要这篇论文

Answer in order:

1. What is the real-world or research bottleneck?
2. Why do existing methods fail or leave performance on the table?
3. What observation unlocks the new method?
4. What is the main lever: better modeling, better optimization, better system scheduling, better data, or a cleaner theoretical framing?

## 3. Fast-Read View / 速读版

- Five-sentence story / 五句话讲完整篇 paper
- Three core takeaways / 三个核心 takeaways
- The one figure/table to remember / 最值得记住的图或表
- 60-second public script / 60 秒大众口播

## 4. Deep-Read View / 精读版

- Problem setup / 问题设定
- Core intuition / 核心直觉
- Method components / 方法组件
- Algorithm flow / 算法流程
- Key equations or notation / 关键公式或符号
- Training or inference procedure / 训练或推理流程
- Experiments and baselines / 实验和 baseline
- Ablations / 消融
- Limitations and unanswered questions / 局限和待追问

## 5. Concept Ladder / 概念三层解释

For every core concept, write:

```text
Concept / 概念:
Plain language / 白话:
Analogy / 类比:
Where the analogy breaks / 类比边界:
Technical explanation / 技术解释:
Evidence / 论文依据:
```

Use at least 3 concepts for substantial papers.

## 6. Algorithm Walkthrough / 算法跑一遍

Use a toy example. Prefer small numbers and visible state transitions.

Required format:

1. Input
2. State before step
3. Operation
4. State after step
5. Why this step helps

If the method is not algorithmic, replace this with a pipeline walkthrough.

## 7. Evidence Ledger / 证据账本

Use this table:

| Claim | Evidence | Strength | Caveat |
|---|---|---|---|
| Paper claim | Section/Figure/Table/Eq/URL | strong/medium/weak | What could weaken it |

## 8. Retelling Kit / 转述工具包

- 60-second script / 60 秒版
- 3-minute script / 3 分钟版
- Nontechnical friend version / 非技术朋友版
- ML engineer version / 工程师版
- 5 likely questions and answers / 5 个可能被问到的问题

## 9. Bilingual Style / 双语风格

When bilingual output is requested:

- Use Chinese as the main explanatory language if the user writes in Chinese.
- Keep key technical terms in English alongside Chinese, e.g. `投机解码 speculative decoding`.
- Put concise English mirrors under major points, not a full duplicate translation unless requested.
- Avoid literal translation. Preserve meaning and teaching clarity.
