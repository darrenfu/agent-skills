# SQLite State Reference

Use PointClaw SQLite as the canonical database contract. `schema/001_init.sql` is retained for legacy Churn Fu SQLite compatibility only.

## Bootstrap

```bash
sqlite3 --version
python3 <PLUGIN_ROOT>/scripts/churnfu.py init-db
python3 <PLUGIN_ROOT>/scripts/churnfu.py status
```

## Write Rules

- Store card inventory in PointClaw tables only: `account_owner`, `issuer`, `card_product`, and `card_instance`.
- Do not create cards in legacy Churn Fu SQLite; card inventory belongs in PointClaw.
- Do not treat `card_product.product_name` as unique. Use `card_instance.card_id`, with `card_instance.last_digits` when visible, for duplicate product names.
- Append benefit usage observations to PointClaw `benefit_status_snapshot`, linked through `card_benefit`.
- Append count-based benefit observations, such as Paze 10-use counters, to `benefit_counter_snapshot`, linked through `card_benefit` and `holder_owner_id`.
- If legacy Churn Fu benefit usage is newer, sync it into PointClaw only through existing PointClaw cards and benefits.
- Record each import or portal capture in `capture_run`.
- Use `v_action_items` and `v_benefit_automation_candidates` for suggested opportunities.
- Store durable action plans in `benefit_action_opportunity`, action rules in `benefit_automation_rule`, and prepared/submitted outcomes in `benefit_redemption_attempt` when the workflow creates durable action state.
- Use `card_reconciliation_issue` for durable card/benefit reconciliation problems when the PointClaw schema supports it; otherwise report blockers in the session output without mutating card inventory.
- Do not commit generated `.sqlite` or `.db` files.

## Main Views

Use these views first:

```sql
SELECT * FROM v_live_cards;
SELECT * FROM v_latest_benefit_status;
SELECT * FROM v_latest_benefit_counter_status;
SELECT * FROM v_action_items;
SELECT * FROM v_benefit_automation_candidates;
```

Use direct table queries only when the views do not contain enough context.

## State Transition Pattern

1. Insert or update `account_owner`, `issuer`, `card_product`, and `card_instance` only when the workflow is explicitly authorized to change inventory.
2. Insert reusable benefit definitions into `benefit_definition` and link cards through `card_benefit`.
3. Insert a `capture_run` for every portal, import, or manual evidence pass.
4. Insert current usage observations into `benefit_status_snapshot`.
5. For count-based benefits where a primary cardholder and authorized user each receive separate allowances, insert separate `benefit_counter_snapshot` rows with different `holder_owner_id` and `participant_role`.
6. Insert durable opportunities into `benefit_action_opportunity` only when the user asked Churn Fu to track that plan.
7. Insert prepared/submitted action outcomes into `benefit_redemption_attempt` only after user-confirmed workflow progress.
8. Insert unresolved durable reconciliation issues into `card_reconciliation_issue` when applicable.

## Validation Queries

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

## Completion Criteria

The state layer is ready only when:

- The configured database validates as PointClaw or explicitly requested legacy Churn Fu SQLite.
- `PRAGMA foreign_key_check` returns no rows.
- Sensitive raw identifiers are not stored, except local card last four digits used for duplicate-card disambiguation and payment-method mapping.
- Session blockers accurately describe user-required actions, and durable PointClaw reconciliation issues are recorded in PointClaw tables only when the schema supports them.
