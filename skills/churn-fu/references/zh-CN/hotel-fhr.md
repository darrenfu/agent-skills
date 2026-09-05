# Hotel FHR Placeholder

这个文件只是未来 hotel portal / Fine Hotels + Resorts workflow 的 placeholder。

Do not use for live execution.

## 当前状态

- FHR execution workflow 尚未实现。
- 不要为 FHR 打开 live issuer travel portal。
- 不要为 FHR search、rank、book、change、cancel 或 submit payment。
- 不要为 FHR transaction 请求 site authorization。
- 不要从 Hilton semi-flex workflow 推断 FHR policy 或 booking rules。

## 允许做的事

- 记录用户 requirements、constraints 和 open questions。
- 用户明确要求时，记录 public official-source research notes。
- 起草未来 workflow proposal，等待用户 review。
- notes 保持非敏感；除非用户要求 repo update，不写入 committed runtime state。

## 未来实现 checklist

这个文件变成可执行 workflow 前，需要补齐：

- Official booking-channel eligibility rules。
- Login 和 portal handoff rules。
- Search、ranking 和 cancellation-policy rules。
- Payment mapping 和 confirmation scope。
- SQLite state model 和 dry-run evals。
- 先失败后通过的 contract tests。
