# 信用卡管理工作流

完成 setup 后，使用本文件作为跨 issuer 管理流程的 canonical reference。当前支持的 issuer adapter 只有 Amex，但本 reference 保留 issuer-agnostic 结构，方便未来扩展。

## 范围输入

用 PointClaw identifiers 或明确 scope value 追踪：

| Field | 含义 |
|---|---|
| `owner_scope` | `account_owner.owner_id` 列表；尚未选择精确 id 时可用 owner display labels |
| `issuer_scope` | Amex only、selected issuers，或未来 all-issuer scope |
| `benefit_scope` | all benefits、airline credits、hotel credits、FHR，或 selected benefits |
| `execution_scope` | audit-only、prepare-only，或 user-confirmed execution |
| `session_output_mode` | chat、markdown artifact、local file，或 repository update |

## Step 1.b 语义一致性验证

使用迁移后的 reference 执行前，先验证所选语言 reference set 是否表达了当前 Churn Fu session 要求的同等语义和功能：

- PointClaw SQLite 是持久 truth source。
- 当前实现只支持 Amex。
- Chrome autofill 只能通过用户批准的可见账号建议使用。
- Passwords、MFA、CAPTCHA、CVV、passkeys 和 identity verification 由用户处理。
- Card product name 不是唯一标识；使用 `card_instance.card_id`，可见时再结合 `card_instance.last_digits`。
- Benefit definitions 优先来自 official issuer terms；account-specific usage 来自 portal、statement、transaction 或 user evidence。
- 用户确认型外部副作用必须停在 purchase、booking、change、cancellation、enrollment、redemption 或 payment submission 前。
- Southwest airline credit 执行使用对应语言的 `airline-credit-southwest.md`。
- Hotel credit planning 可以读取对应语言的 `hotel-fhr.md`，但 FHR is a placeholder，不是可执行 workflow。
- FHR is a placeholder，直到用户明确实现它。

如果缺失或矛盾任何必要语义，停止并先更新 reference，不要执行。

## 认证和用户交接

1. 任何 browser login 或 portal handoff 前，先读取 `login-flows.md`。
2. 使用 fresh browser session，除非用户明确要求复用已有 authenticated session。
3. 只有当可见多个 saved login 或 account context 时，才询问使用哪个可见 login 或 owner display label。
4. 不读取、展示、导出或持久化 credentials、cookies、tokens、local storage 或 browser password database contents。
5. 遇到 password entry、passkey、OTP/MFA、CAPTCHA、CVV 或 identity verification，停止并让用户完成。
6. 认证后，先验证可见 account context，再读取 card 或 benefit data。

通过以下至少一项验证 account context：

- 网站显示的 owner display label 或 login label
- card list 与预期 issuer/account scope 一致
- 用户确认 account context

如果 account context 错误或模糊，停止并要求用户切换账号。

## 卡片 Inventory

每张卡分类为：

- `live`
- `closed`
- `pending_activation`
- `authorized_user_only`
- `downgraded`
- `upgraded`
- `product_changed`
- `unknown`
- `blocked`

Discovery source 优先级：

1. 用户同意后的 logged-in issuer portal。
2. 用户提供的 card list 或 export。
3. 用户授权的 aggregator account data。
4. Transaction 或 statement evidence。
5. 用户手动确认。

记录：

| Field | 含义 |
|---|---|
| `owner_id` | PointClaw `account_owner.owner_id` |
| `owner_label` | PointClaw `account_owner.display_label` |
| `issuer_name` | PointClaw `issuer.issuer_name` |
| `card_id` | 稳定的 PointClaw `card_instance.card_id` |
| `card_label` | PointClaw `card_instance.display_label` |
| `product_name` | Public product name；不唯一 |
| `last_digits` | 可见 card last four；默认保存 |
| `role` | primary / authorized user / business / employee |
| `card_state` | card lifecycle state |
| `opened_date` | known、approximate 或 unknown |
| `annual_fee_date` | known、approximate 或 unknown |
| `source` | evidence source |
| `confidence` | evidence confidence |
| `checked_at` | timestamp |

PointClaw 映射：

| Logical field | PointClaw table.column |
|---|---|
| owner/account | `account_owner.display_label` / `account_owner.owner_id` |
| issuer | `issuer.issuer_name` |
| product | `card_product.product_name`, `card_product.network`, `card_product.card_family` |
| card id | `card_instance.card_id` |
| card label | `card_instance.display_label` |
| last four | `card_instance.last_digits` |
| lifecycle state | `card_instance.card_state` |
| opened/closed dates | `card_instance.opened_at`, `card_instance.closed_at` |
| evidence/source | `card_instance.source_system`, `card_instance.source_key` |

同步新增和关闭卡：

1. 比较当前 portal inventory 和 SQLite state。
2. 用稳定的 `card_instance.card_id` 匹配；owner、issuer、product name 和 `last_digits` 作为辅助 evidence。
3. 只有用户明确要求更新 inventory 时，才把新出现的卡标记为 insert candidate。
4. 缺失的卡标记为 possibly closed or hidden。
5. 没有用户确认，不要删除缺失卡。
6. Lifecycle events 与当前 state 分开记录。

## 福利 Catalog

理论 benefit definitions 的 source order：

1. Official issuer card terms、benefit guides、program terms 和 product pages。
2. 用户同意后的 logged-in issuer portal benefit pages。
3. 未来版本如启用 CardPointers，只作为 secondary catalog enrichment 和 cross-check。
4. 其他 public sources 只能明确标记为 advisory。

Official public terms 优先用于 reusable catalog definitions。Logged-in issuer pages 用于：

- benefit 因 cardholder 或 targeted offer 不同
- benefit 需要 enrollment status
- issuer 只向 cardmember 暴露相关 terms
- usage status、remaining amount 或 deadline 是 account-specific

如果 official terms 需要登录，要求 portal handoff 或用户提供 evidence。不要绕过 login、paywalls 或 identity checks。

记录：

| Field | 含义 |
|---|---|
| `issuer_name` | Issuer 或 network |
| `product_name` | Public card product name |
| `benefit_id` | PointClaw `benefit_definition.benefit_id` |
| `card_benefit_id` | Link 到 card 后的 PointClaw `card_benefit.card_benefit_id` |
| `benefit_name` | 可用时记录 official name |
| `benefit_type` | airline_credit / hotel_credit / dining_credit / portal_credit / lounge / status / insurance / offer / other |
| `period` | annual / semiannual / quarterly / monthly / per-trip / one-time / unknown |
| `cap_amount` | dollar cap 或 qualitative benefit |
| `reset_rule` | calendar year、cardmember year、statement cycle、quarter、unknown |
| `eligibility` | merchants、booking channel、enrollment rule |
| `exclusions` | known exclusions |
| `source_label` | source label；敏感时不存 private URL |
| `source_rank` | official_terms / issuer_portal / cardpointers / advisory |
| `confidence` | official_terms / secondary_catalog / inferred / unknown |

PointClaw 映射：

| Logical field | PointClaw table.column |
|---|---|
| benefit definition | `benefit_definition.benefit_id`, `benefit_definition.benefit_name` |
| category/type | `benefit_category.category_id`, `benefit_category.category_name`, `benefit_definition.benefit_kind` |
| cadence/period | `benefit_definition.cadence` |
| official amount | `benefit_definition.official_amount_cents` |
| threshold | `benefit_definition.official_threshold_cents` |
| enrollment flag | `benefit_definition.enrollment_required` |
| card linkage | `card_benefit.card_benefit_id`, `card_benefit.card_id`, `card_benefit.benefit_id` |

如果 official terms 和 secondary catalog 冲突：

1. 优先 official terms。
2. 保留 secondary note 作为 evidence。
3. 在 report 中标记冲突。
4. official terms 不可用或冲突时，不要仅凭 secondary data 执行动作。

## 使用状态 Audit

Usage status 是 account-specific，不能从 public catalog 推断。

Evidence priority：

1. Issuer portal benefit tracker 或 benefit page。
2. Card account 上 posted statement credits。
3. Transactions 加 matched statement credits。
4. 用户提供的 statement screenshots 或 exports。
5. 用户确认，标记为 `user_confirmed`。

记录：

| Field | 含义 |
|---|---|
| `owner_id` | PointClaw `account_owner.owner_id` |
| `owner_label` | PointClaw `account_owner.display_label` |
| `issuer_name` | PointClaw `issuer.issuer_name` |
| `card_id` | PointClaw `card_instance.card_id` |
| `card_benefit_id` | PointClaw `card_benefit.card_benefit_id` |
| `period_start` | current period start |
| `period_end` | current period end |
| `cap_amount` | benefit cap |
| `used_amount` | verified 或 unknown |
| `remaining_amount` | verified、calculated 或 unknown |
| `enrollment_status` | enrolled / not_enrolled / not_required / unknown |
| `usage_status` | unused / partially_used / fully_used / pending_credit / not_found_in_portal / reversed / unknown / blocked |
| `evidence` | portal / statement_credit / transaction / user / unknown |
| `confidence` | portal_verified / transaction_verified / statement_credit_verified / user_confirmed / inferred / unknown |
| `checked_at` | timestamp |

PointClaw 映射：

| Logical field | PointClaw table.column |
|---|---|
| capture/evidence run | `capture_run.run_id`, `capture_run.captured_at`, `capture_run.source_system`, `capture_run.source_mode` |
| card benefit | `card_benefit.card_benefit_id` |
| period | `benefit_status_snapshot.period_type`, `period_label`, `period_start`, `period_end` |
| status | `benefit_status_snapshot.status_code` |
| used amount | `benefit_status_snapshot.used_amount_cents` |
| cap amount | `benefit_status_snapshot.limit_amount_cents` |
| remaining amount | `benefit_status_snapshot.remaining_amount_cents` |
| confidence | `benefit_status_snapshot.confidence` |
| raw tracker text | `benefit_status_snapshot.tracker_text` |

规则：

- Issuer portal 如果显示 used 和 remaining amount，作为 current-session source of truth。
- Transaction 显示可能使用但 credit 未 post，标记 `pending_credit`。
- Credit posted 后 reversed，标记 `reversed`。
- Catalog benefit 在 portal 中找不到，标记 `not_found_in_portal`。
- Benefit 需要 enrollment 但 enrollment status unknown，标记 `blocked`。

## Action Candidate Selection

Benefit 只有满足以下条件才能成为 action candidate：

1. 当前周期仍有 remaining value，或 qualitative benefit 仍可用。
2. Source confidence 足以行动。
3. Required merchant、channel、date window 或 enrollment rule 清楚。
4. 用户授权该 benefit category 的 planning。
5. Action 不需要猜测 card、payment、reservation 或 account mappings。

以下情况不要选择 candidate：

- usage status unknown 且用户未接受不确定性
- terms unclear 或 sources 冲突
- payment method mapping 模糊
- action 可能违反 terms 或需要 deception
- final purchase、booking、cancellation、redemption 或 enrollment 会在没有用户确认时发生

排序：

1. Expiration urgency
2. Remaining value
3. Confidence
4. Execution effort
5. Reversal 或 clawback risk

如果 PointClaw schema 支持该 action，把 candidate plan 记录到 `benefit_action_opportunity`；否则写入 session output：

| Field | 含义 |
|---|---|
| `opportunity_id` | PointClaw `benefit_action_opportunity.opportunity_id`，或 session-local id |
| `card_id` | PointClaw `card_instance.card_id` |
| `card_benefit_id` | PointClaw `card_benefit.card_benefit_id` |
| `remaining_value` | dollar 或 qualitative value |
| `deadline` | expiration 或 reset |
| `workflow_name` | executable reference 或 workflow name |
| `required_user_actions` | login、payment、confirmation、upload 等 |
| `expected_cost` | estimated cost |
| `expected_recovery` | expected credit 或 value |
| `risk_level` | low / medium / high / unknown |
| `risk_notes` | concise notes |
| `source_confidence` | confidence value |

## Post-Action Monitoring

Benefit action 产生 transaction、booking、change、cancellation、enrollment 或 redemption 后使用本节。

Evidence priority：

1. Statement credit line item。
2. Issuer benefit tracker。
3. Transaction record。
4. 用户提供的 statement evidence。
5. 用户确认。

Status values：

- `pending`
- `posted`
- `partially_posted`
- `not_posted`
- `reversed`
- `expired`
- `blocked`

规则：

- Credit 或 usage 未验证前，不要把 benefit 标记为 used。
- 如果 refund 发生在 credit post 前，继续 monitoring。
- 如果 credit post 后 reverse，且 issuer tracker evidence 支持，则 reopen benefit。
- 如果 period expires，把 residual value 标记为 missed 或 unknown。

## 完成标准

Session 只有在以下条件满足时才算完成：

- 每张 scoped card 都分类为 live、closed、blocked 或 out of scope
- 每个 scoped benefit 都分类为 verified、inferred、unknown 或 blocked
- 每个 suggested action 都有 source、amount、deadline、risk 和 required user action
- 所有 irreversible actions 都已明确确认，或留作 handoff
- SQLite state 通过 `PRAGMA foreign_key_check`
