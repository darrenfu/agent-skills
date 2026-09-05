# SQLite 状态

使用 PointClaw SQLite 作为 canonical database contract。`schema/001_init.sql` 只保留给 legacy Churn Fu SQLite 兼容使用。

## 初始化

```bash
sqlite3 --version
python3 <PLUGIN_ROOT>/scripts/churnfu.py init-db
python3 <PLUGIN_ROOT>/scripts/churnfu.py status
```

## 写入规则

- 存 alias，不存敏感标识符；例外是本地未提交 SQLite state 默认保存可见 card last four。
- 默认 card inventory 只写 PointClaw tables：`account_owner`、`issuer`、`card_product`、`card_instance`。
- 不要在 legacy Churn Fu SQLite 里创建卡；card inventory 属于 PointClaw。
- 不要把 `card_product.product_name` 当唯一标识。同名产品用 `card_instance.card_id` 区分；可见时再结合 `card_instance.last_digits`。
- usage observation 追加写入 PointClaw `benefit_status_snapshot`，并通过 `card_benefit` 关联。
- Paze 这类按次数记账的 benefit observation 追加写入 `benefit_counter_snapshot`，并通过 `card_benefit` 和 `holder_owner_id` 关联。
- 如果 legacy Churn Fu benefit usage 更新，只能通过已存在的 PointClaw cards 和 benefits 同步进 PointClaw。
- 每次 portal/import/manual evidence pass 写一条 `capture_run`。
- 使用 `v_action_items` 和 `v_benefit_automation_candidates` 查看 suggested opportunities。
- workflow 产生 durable action state 时，durable action plans 写入 `benefit_action_opportunity`，action rules 写入 `benefit_automation_rule`，prepared/submitted outcomes 写入 `benefit_redemption_attempt`。
- 用户需要处理的问题优先在 session output 中报告；需要持久化且 PointClaw schema 支持时写入 `card_reconciliation_issue`。
- 不要提交生成的 `.sqlite` 或 `.db` 文件。

## 主要视图

优先使用：

```sql
SELECT * FROM v_live_cards;
SELECT * FROM v_latest_benefit_status;
SELECT * FROM v_latest_benefit_counter_status;
SELECT * FROM v_action_items;
SELECT * FROM v_benefit_automation_candidates;
```

只有当 view 信息不足时，才直接查询底层表。

## State transition pattern

1. 只有明确授权改变 inventory 时，才 insert/update `account_owner`、`issuer`、`card_product`、`card_instance`。
2. 把 reusable benefit definitions 写入 `benefit_definition`，并通过 `card_benefit` 关联到 card。
3. 每次 portal、import 或 manual evidence pass 写入 `capture_run`。
4. 把当前 usage observations 追加写入 `benefit_status_snapshot`。
5. 对 Paze 这类主卡和副卡各有独立 allowance 的 count-based benefit，用不同的 `holder_owner_id` 和 `participant_role` 写入多条 `benefit_counter_snapshot`。
6. 只有当用户要求 Churn Fu 追踪该 plan 时，才把 durable opportunities 写入 `benefit_action_opportunity`。
7. 只有 user-confirmed workflow 有进展后，才把 prepared/submitted action outcomes 写入 `benefit_redemption_attempt`。
8. 持久 unresolved reconciliation issue 时使用 `card_reconciliation_issue`。

## Validation queries

```sql
PRAGMA foreign_key_check;

SELECT owner_label, issuer_name, product_name, card_label, last_digits, opened_at, next_anniversary_at
FROM v_live_cards
ORDER BY owner_label, issuer_name, product_name, card_label;

SELECT owner_label, card_label, product_name, category_name, benefit_name,
       period_type, period_label, status_code,
       used_amount_cents, limit_amount_cents, remaining_amount_cents,
       confidence, captured_at
FROM v_latest_benefit_status
ORDER BY owner_label, card_label, benefit_name, captured_at DESC;

SELECT priority_rank, owner_label, card_label, category_name, benefit_name,
       status_code, remaining_display, confidence
FROM v_action_items
ORDER BY priority_rank, category_name, benefit_name, card_label;

SELECT source_owner_label, holder_owner_label, card_label, benefit_name,
       participant_role, wallet_provider, used_count, limit_count, remaining_count
FROM v_latest_benefit_counter_status
ORDER BY holder_owner_label, source_owner_label, card_label, benefit_name;
```

## 完成标准

State layer 只有在以下条件满足时才 ready：

- 配置的数据库可验证为 PointClaw；或在明确请求 legacy 时验证为 Churn Fu SQLite。
- `PRAGMA foreign_key_check` 返回空结果。
- 不存敏感 raw identifiers，除了用于同名卡区分和 payment-method mapping 的本地 card last four。
- Session blockers 准确描述用户需要处理的 actions；需要持久化的 PointClaw reconciliation issue 只写 PointClaw 支持的表。
