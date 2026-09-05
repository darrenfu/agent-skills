---
name: churn-fu
description: Bilingual English and Simplified Chinese SQLite-first credit card lifecycle and benefits operations. Use when setting up Churn Fu, managing cards or benefits, preparing airline or hotel workflows, or activating a Visa virtual gift card and applying its full balance to a Puget Sound Energy (PSE) account before removing the temporary wallet card.
---

# Churn Fu

[English](#en) | [简体中文](#zh-cn)

<a id="en"></a>
## English

[Switch to 简体中文](#zh-cn)

Use this skill to operate the Churn Fu toolkit. Churn Fu is issuer-agnostic by design, but the current implementation supports Amex only. CardPointers enrichment is intentionally disabled in this version.

### Language

Support English and Simplified Chinese.

- If the user writes in English, use `references/en-US/`.
- If the user writes in Simplified Chinese, use `references/zh-CN/`.
- If mixed or unclear, match the user's latest message.
- Keep database aliases non-sensitive in either language.
- Keep CLI config `language` as `auto` unless the user explicitly requests `en-US` or `zh-CN`.

### Operating Rules

1. Treat PointClaw SQLite as the source of truth.
2. Run deterministic scripts for setup and state checks instead of improvising SQL.
3. Use aliases for people, accounts, cards, payment methods, and reservations.
4. Never store passwords, OTPs, cookies, tokens, CVV, full card numbers, or full reservation confirmations.
5. Store visible card last four digits by default in local uncommitted SQLite state.
6. Let the user handle passwords, MFA, CAPTCHA, CVV, and final external side effects.
7. Stop before purchase, booking, change, cancellation, enrollment, redemption, or payment unless an active site-level batch authorization covers that site and action.
8. For transaction-making workflows, ask one confirmation per site per live run with exact site, account, amount ceiling, eligible actions, payment mappings, benefits, and risk; treat it as a site-level batch authorization.

### First Action

For any browser login or portal handoff:

1. Read the matching language version of `login-flows.md` before opening issuer, airline, hotel, merchant, Gmail, gift-card access, or travel portal pages.
2. Use only visible user-approved Chrome autofill or already-authenticated sessions.
3. Stop on MFA, CAPTCHA, passkey, CVV, identity verification, payment verification, wrong account, or final external submit not covered by an active site-level batch authorization.

For setup or first use:

1. Read `references/en-US/setup.md` for English or `references/zh-CN/setup.md` for Simplified Chinese.
1.b. Read `credit-card-management.md` in the same language and verify the reference set expresses the same semantics and functionality required by this Churn Fu session before execution.
2. Run `python3 <PLUGIN_ROOT>/scripts/churnfu.py doctor`.
3. If `sqlite3` is missing, follow the matching language version of `mcp-installer-policy.md`.
4. Read the matching language version of `first-run-config.md`.
5. Run `config-wizard`, `init-db`, and `validate` with defaults.
6. Ask setup questions only when the defaults are blocked or ambiguous.

For Amex card or benefit audit:

1. Read the matching language version of `credit-card-management.md`.
2. Read the matching language version of `amex-workflow.md`.
3. Read the matching language version of `sqlite-state.md`.
4. Read the matching language version of `safety-confirmations.md` if action planning or external handoff is in scope.

For airline credit execution:

1. Read the matching language version of `airline-credit-southwest.md`.
2. Read the matching language version of `safety-confirmations.md`.
3. Prepare the plan from SQLite state.
4. Obtain or verify a site-level batch authorization for the airline site before the first transaction submit in the live run.
5. When the user asks the agent to continue a Southwest change loop, the agent may autonomously open each eligible reservation, search same-route/same-date or nearby eligible options, choose a reasonable additional fare difference closest to the workflow target while avoiding large overage or add-ons, and submit covered changes within the site-level batch authorization. Reconfirm only if the site, account, amount ceiling, payment mapping, route/date/fare rules, or risk envelope changes.

For hotel or FHR requests:

1. Read the matching language version of `hotel-fhr.md`.
2. Treat FHR as a placeholder, not an executable workflow.
3. Do not open a live travel portal, request site-level batch authorization, book, change, cancel, or submit payment for FHR.
4. Capture requirements or user notes only until the workflow is explicitly implemented.

For Hilton semi-flex credit execution:

1. Read the matching language version of `hilton-semiflex-credit.md`.
2. Read the matching language version of `safety-confirmations.md`.
3. Run `python3 <PLUGIN_ROOT>/scripts/churnfu.py hilton-semiflex-dry-run --as-of YYYY-MM-DD` before live execution.
4. Prepare the plan from SQLite state.
5. Obtain or verify a site-level batch authorization for Hilton before the first booking/refund/cancellation submit in the live run.

For Visa VGC to PSE execution:

1. Read `references/en-US/vgc-pse.md`.
2. Read `references/en-US/login-flows.md` and `references/en-US/safety-confirmations.md`.
3. Treat one user request to activate the supplied VGC, pay its full balance to the identified PSE account, and remove the temporary wallet card as one workflow authorization.
4. Do not add Churn Fu per-step confirmations for expected wallet-add, duplicate-payment/AutoPay warning, payment-submit, or wallet-removal transitions inside that authorization. Always obey confirmation and handoff requirements enforced by repository security policy, the host browser, or the Codex runtime.

### Path Resolution

The skill directory is `<PLUGIN_ROOT>/skills/churn-fu`. The plugin root is two directories above this skill directory.

Use:

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py <command>
```

Default state is `<PLUGIN_ROOT>/../pointclaw-data/pointclaw.sqlite`. The old `<PLUGIN_ROOT>/skills/churn-fu/local/churn-fu.sqlite` file is legacy/BC-only; use it only when explicitly reading or syncing legacy Churn Fu state.

<a id="zh-cn"></a>
## 简体中文

[切换到 English](#en)

使用本 skill 操作 Churn Fu toolkit。Churn Fu 的设计是 issuer-agnostic，但当前实现只支持 Amex。CardPointers enrichment 在当前版本中有意禁用。

### 语言

支持 English 和简体中文。

- 如果用户使用 English，读取 `references/en-US/`。
- 如果用户使用简体中文，读取 `references/zh-CN/`。
- 如果语言混合或不明确，匹配用户最新消息。
- 任一语言下，数据库 alias 都必须保持非敏感。
- 除非用户明确要求 `en-US` 或 `zh-CN`，CLI config 中的 `language` 保持 `auto`。

### 操作规则

1. 把 PointClaw SQLite 视为 truth source。
2. 设置和状态检查使用确定性脚本，不要临场拼 SQL。
3. 对 people、accounts、cards、payment methods 和 reservations 使用 aliases。
4. 不存 passwords、OTPs、cookies、tokens、CVV、full card numbers 或 full reservation confirmations。
5. 本地未提交 SQLite state 默认保存可见 card last four。
6. Passwords、MFA、CAPTCHA、CVV 和最终外部副作用由用户处理。
7. Purchase、booking、change、cancellation、enrollment、redemption 或 payment 前必须停止，除非该网站和动作已被 active site-level batch authorization 覆盖。
8. 涉及 make transaction 的 workflow，每个网站每个 live run 只确认一次；确认内容必须包含 site、account、amount ceiling、eligible actions、payment mappings、benefits 和 risk，并作为 site-level batch authorization。

### 首次动作

任何 browser login 或 portal handoff：

1. 打开 issuer、airline、hotel、merchant、Gmail、gift-card access 或 travel portal 页面前，先读取对应语言版本的 `login-flows.md`。
2. 只使用用户批准的可见 Chrome autofill 或已登录 session。
3. 遇到 MFA、CAPTCHA、passkey、CVV、identity verification、payment verification、wrong account，或未被 active site-level batch authorization 覆盖的最终外部提交，停止。

设置或首次使用：

1. English 读取 `references/en-US/setup.md`；简体中文读取 `references/zh-CN/setup.md`。
1.b. 读取同语言的 `credit-card-management.md`，并在执行前验证 reference set 表达了当前 Churn Fu session 所需的同等语义和功能。
2. 运行 `python3 <PLUGIN_ROOT>/scripts/churnfu.py doctor`。
3. 如果缺少 `sqlite3`，遵循对应语言版本的 `mcp-installer-policy.md`。
4. 读取对应语言版本的 `first-run-config.md`。
5. 使用默认值运行 `config-wizard`、`init-db` 和 `validate`。
6. 只有默认值被阻塞或有歧义时才提问。

Amex card 或 benefit audit：

1. 读取对应语言版本的 `credit-card-management.md`。
2. 读取对应语言版本的 `amex-workflow.md`。
3. 读取对应语言版本的 `sqlite-state.md`。
4. 如果包含 action planning 或 external handoff，读取对应语言版本的 `safety-confirmations.md`。

Airline credit 执行：

1. 读取对应语言版本的 `airline-credit-southwest.md`。
2. 读取对应语言版本的 `safety-confirmations.md`。
3. 从 SQLite state 准备计划。
4. live run 第一次 transaction submit 前，为 airline site 获取或验证 site-level batch authorization。
5. 当用户要求 agent 继续 Southwest change loop 时，agent 可以自动逐笔打开 eligible reservation，搜索同路线/同日期或附近 eligible 选项，选择最接近 workflow target 且避免大额 overage 或 add-ons 的合理 additional fare difference，并在 site-level batch authorization 覆盖范围内提交 change。只有 site、account、amount ceiling、payment mapping、route/date/fare rules 或 risk envelope 变化时才重新确认。

Hotel 或 FHR 请求：

1. 读取对应语言版本的 `hotel-fhr.md`。
2. 把 FHR 当作 placeholder，不作为可执行 workflow。
3. 不打开 live travel portal，不请求 site-level batch authorization，不为 FHR booking、change、cancel 或 submit payment。
4. 在 workflow 明确实现前，只记录需求或用户 notes。

Hilton semi-flex credit 执行：

1. 读取对应语言版本的 `hilton-semiflex-credit.md`。
2. 读取对应语言版本的 `safety-confirmations.md`。
3. live 执行前先运行 `python3 <PLUGIN_ROOT>/scripts/churnfu.py hilton-semiflex-dry-run --as-of YYYY-MM-DD`。
4. 从 SQLite state 准备计划。
5. live run 第一次 booking/refund/cancellation submit 前，为 Hilton 获取或验证 site-level batch authorization。

Visa VGC 到 PSE 执行：

1. 读取 `references/zh-CN/vgc-pse.md`。
2. 读取 `references/zh-CN/login-flows.md` 和 `references/zh-CN/safety-confirmations.md`。
3. 用户一次性要求激活所提供的 VGC、把全部余额付入指定 PSE 账户并删除临时 wallet card 时，把它视为一个完整 workflow authorization。
4. 只要仍在该 authorization 范围内，不为预期的 wallet add、duplicate-payment/AutoPay warning、payment submit 或 wallet removal 增加 Churn Fu 自己的逐步确认。始终遵守 repository security policy、host browser 或 Codex runtime 强制执行的确认和 handoff 要求。

### 路径解析

Skill 目录是 `<PLUGIN_ROOT>/skills/churn-fu`。Plugin root 是 skill 目录向上两级。

使用：

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py <command>
```

默认状态位于 `<PLUGIN_ROOT>/../pointclaw-data/pointclaw.sqlite`。旧的 `<PLUGIN_ROOT>/skills/churn-fu/local/churn-fu.sqlite` 只用于 legacy/BC 读取或同步，不再作为卡片 inventory truth source。
