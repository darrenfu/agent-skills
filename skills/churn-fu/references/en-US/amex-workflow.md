# Amex Workflow Reference

Use this for the first supported issuer adapter.

## Scope

- Supported issuer: Amex.
- Supported tasks: card inventory, benefit catalog discovery, usage status audit, enrollment status, statement credit monitoring.
- Unsupported in this version: automatic credential entry, CardPointers enrichment, non-Amex issuers.

## Login

1. Read `login-flows.md` and follow its American Express section before opening the portal.
2. Open Amex portal only if the user allowed portal handoff.
3. After login, use the selected Amex login only as a runtime login label unless the user provides another non-sensitive PointClaw owner label.
4. Verify the account context by visible portal state or user confirmation.

## Card Inventory

For each visible card:

- Match or assign PointClaw `card_instance.card_id`.
- Store public product name in `card_product.product_name`.
- Store visible card last four in `card_instance.last_digits`.
- Classify lifecycle state in `card_instance.card_state`.
- Treat product name as non-unique. Use `card_instance.card_id`, plus `card_instance.last_digits` when available, to distinguish duplicate card products.

## Benefit Catalog

Use source order:

1. Official Amex product terms and benefit guides.
2. Logged-in Amex benefit pages for account-specific or cardmember-only terms.

CardPointers enrichment is disabled in this version.

## Usage Status

Usage status can come from:

- Amex benefit tracker
- statement credit
- transaction plus credit evidence
- user confirmation

Public terms define benefits. They do not prove used or remaining amount.

Write current-period usage to PointClaw `benefit_status_snapshot`, linked through `card_benefit.card_benefit_id`; record each evidence pass in `capture_run`.
