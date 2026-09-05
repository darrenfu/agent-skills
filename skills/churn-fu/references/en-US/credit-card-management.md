# Credit Card Management Reference

Use this as the canonical cross-issuer management workflow after setup. The current supported issuer adapter is Amex only, but this reference preserves issuer-agnostic structure for future adapters.

## Scope Inputs

Track these session inputs as PointClaw identifiers or explicit scope values:

| Field | Meaning |
|---|---|
| `owner_scope` | `account_owner.owner_id` values, or owner display labels when the user has not selected exact ids yet |
| `issuer_scope` | Amex only, selected issuers, or future all-issuer scope |
| `benefit_scope` | all benefits, airline credits, hotel credits, FHR, or selected benefits |
| `execution_scope` | audit-only, prepare-only, or user-confirmed execution |
| `session_output_mode` | chat, markdown artifact, local file, or repository update |

## Step 1.b Semantic Parity Verification

Before using migrated reference content for execution, verify that the selected language reference set expresses the same semantics and functionality required by the current Churn Fu session:

- PointClaw SQLite is the durable source of truth.
- The current implementation supports Amex only.
- Chrome autofill may be used only through visible user-approved account suggestions.
- Passwords, MFA, CAPTCHA, CVV, passkeys, and identity verification stay with the user.
- Card product names are not unique; use `card_instance.card_id`, plus `card_instance.last_digits` when available.
- Benefit definitions come from official issuer terms first; account-specific usage comes from portal, statement, transaction, or user evidence.
- User-confirmed external side effects must stop before purchase, booking, change, cancellation, enrollment, redemption, or payment submission.
- Southwest airline credit execution uses the language-specific `airline-credit-southwest.md` reference.
- Hotel credit planning can read the language-specific `hotel-fhr.md` reference, but FHR is a placeholder and not an executable workflow.
- FHR is a placeholder until the user explicitly implements it.

If any required semantic is missing or contradicted, stop and update the reference before execution.

## Authentication And User Handoff

1. Read `login-flows.md` before any browser login or portal handoff.
2. Use a fresh browser session unless the user explicitly asks to reuse an existing authenticated session.
3. Ask which visible login or owner display label to use only when multiple saved logins or account contexts are visible.
4. Do not read, reveal, export, or persist credentials, cookies, tokens, local storage, or browser password database contents.
5. Stop and ask the user to complete password entry, passkey, OTP/MFA, CAPTCHA, CVV, or identity verification.
6. After authentication, verify the visible account context before reading card or benefit data.

Verify account context by at least one of:

- owner display label or login label displayed by the site
- card list consistent with expected issuer/account scope
- user-confirmed account context

If the account context is wrong or ambiguous, stop and ask the user to switch accounts.

## Card Inventory

Classify each card as one of:

- `live`
- `closed`
- `pending_activation`
- `authorized_user_only`
- `downgraded`
- `upgraded`
- `product_changed`
- `unknown`
- `blocked`

Use discovery sources in this order:

1. Logged-in issuer portal, with user consent.
2. User-provided card list or export.
3. Aggregator account data, if user authorized.
4. Transaction or statement evidence.
5. Manual user confirmation.

Record:

| Field | Meaning |
|---|---|
| `owner_id` | PointClaw `account_owner.owner_id` |
| `owner_label` | PointClaw `account_owner.display_label` |
| `issuer_name` | PointClaw `issuer.issuer_name` |
| `card_id` | Stable PointClaw `card_instance.card_id` |
| `card_label` | PointClaw `card_instance.display_label` |
| `product_name` | Public product name; not unique |
| `last_digits` | Visible card last four; stored by default when available |
| `role` | primary / authorized user / business / employee |
| `card_state` | card lifecycle state |
| `opened_date` | known, approximate, or unknown |
| `annual_fee_date` | known, approximate, or unknown |
| `source` | evidence source |
| `confidence` | evidence confidence |
| `checked_at` | timestamp |

PointClaw mapping:

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

When syncing new and closed cards:

1. Compare current portal inventory to SQLite state.
2. Match cards by stable `card_instance.card_id`; use owner, issuer, product name, and `last_digits` as supporting evidence.
3. Mark newly visible cards as candidates for insert only when the user explicitly wants inventory updates.
4. Mark missing cards as possibly closed or hidden.
5. Do not delete missing cards without user confirmation.
6. Record lifecycle events separately from current state.

## Benefit Catalog

Discover theoretical benefit definitions using this source order:

1. Official issuer card terms, benefit guides, program terms, and product pages.
2. Logged-in issuer portal benefit pages, only when user consent exists.
3. CardPointers as secondary catalog enrichment and cross-check if enabled in a future version.
4. Other public sources only if explicitly marked as advisory.

Official public terms are preferred for reusable catalog definitions. Logged-in issuer pages are used when:

- the benefit differs by cardholder or targeted offer
- the benefit requires enrollment status
- the issuer exposes relevant terms only to cardmembers
- usage status, remaining amount, or deadline is account-specific

If official terms require login, ask for a portal handoff or user-provided evidence. Do not bypass login, paywalls, or identity checks.

Record:

| Field | Meaning |
|---|---|
| `issuer_name` | Issuer or network |
| `product_name` | Public card product name |
| `benefit_id` | PointClaw `benefit_definition.benefit_id` |
| `card_benefit_id` | PointClaw `card_benefit.card_benefit_id` when linked to a card |
| `benefit_name` | Official name if available |
| `benefit_type` | airline_credit / hotel_credit / dining_credit / portal_credit / lounge / status / insurance / offer / other |
| `period` | annual / semiannual / quarterly / monthly / per-trip / one-time / unknown |
| `cap_amount` | dollar cap or qualitative benefit |
| `reset_rule` | calendar year, cardmember year, statement cycle, quarter, unknown |
| `eligibility` | merchants, booking channel, enrollment rule |
| `exclusions` | known exclusions |
| `source_label` | source label, not private URL if sensitive |
| `source_rank` | official_terms / issuer_portal / cardpointers / advisory |
| `confidence` | official_terms / secondary_catalog / inferred / unknown |

PointClaw mapping:

| Logical field | PointClaw table.column |
|---|---|
| benefit definition | `benefit_definition.benefit_id`, `benefit_definition.benefit_name` |
| category/type | `benefit_category.category_id`, `benefit_category.category_name`, `benefit_definition.benefit_kind` |
| cadence/period | `benefit_definition.cadence` |
| official amount | `benefit_definition.official_amount_cents` |
| threshold | `benefit_definition.official_threshold_cents` |
| enrollment flag | `benefit_definition.enrollment_required` |
| card linkage | `card_benefit.card_benefit_id`, `card_benefit.card_id`, `card_benefit.benefit_id` |

If official terms conflict with a secondary catalog:

1. Prefer official terms.
2. Keep the secondary note as evidence.
3. Mark the conflict in the report.
4. Do not execute an action based solely on secondary data when official terms disagree or are unavailable.

## Usage Status Audit

Usage status is account-specific and cannot be inferred from public catalog data.

Use evidence in this order:

1. Issuer portal benefit tracker or benefit page.
2. Statement credits posted to the card account.
3. Transaction records plus matching statement credits.
4. User-provided statement screenshots or exports.
5. User confirmation, marked as `user_confirmed`.

Record:

| Field | Meaning |
|---|---|
| `owner_id` | PointClaw `account_owner.owner_id` |
| `owner_label` | PointClaw `account_owner.display_label` |
| `issuer_name` | PointClaw `issuer.issuer_name` |
| `card_id` | PointClaw `card_instance.card_id` |
| `card_benefit_id` | PointClaw `card_benefit.card_benefit_id` |
| `period_start` | current period start |
| `period_end` | current period end |
| `cap_amount` | benefit cap |
| `used_amount` | verified or unknown |
| `remaining_amount` | verified, calculated, or unknown |
| `enrollment_status` | enrolled / not_enrolled / not_required / unknown |
| `usage_status` | unused / partially_used / fully_used / pending_credit / not_found_in_portal / reversed / unknown / blocked |
| `evidence` | portal / statement_credit / transaction / user / unknown |
| `confidence` | portal_verified / transaction_verified / statement_credit_verified / user_confirmed / inferred / unknown |
| `checked_at` | timestamp |

PointClaw mapping:

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

Rules:

- If the issuer portal shows used and remaining amounts, treat it as the current-session source of truth.
- If transactions suggest usage but no credit has posted, mark `pending_credit`.
- If a credit posted and later reversed, mark `reversed`.
- If a catalog benefit cannot be found in the portal, mark `not_found_in_portal`.
- If a benefit requires enrollment and enrollment status is unknown, mark `blocked`.

## Action Candidate Selection

A benefit can become an action candidate only when:

1. It has current-period remaining value or a qualitative benefit still available.
2. Its source confidence is strong enough for action.
3. Required merchant, channel, date window, or enrollment rule is clear.
4. The user authorized planning for the benefit category.
5. The action does not require guessing card, payment, reservation, or account mappings.

Do not select candidates when:

- usage status is unknown and the user has not accepted uncertainty
- terms are unclear or conflict across sources
- payment method mapping is ambiguous
- the action could violate terms or requires deception
- final purchase, booking, cancellation, redemption, or enrollment would happen without user confirmation

Rank candidates by:

1. Expiration urgency
2. Remaining value
3. Confidence
4. Execution effort
5. Reversal or clawback risk

Record candidate plans in PointClaw `benefit_action_opportunity` when the schema supports the action, or in session output otherwise:

| Field | Meaning |
|---|---|
| `opportunity_id` | PointClaw `benefit_action_opportunity.opportunity_id`, or session-local id |
| `card_id` | PointClaw `card_instance.card_id` |
| `card_benefit_id` | PointClaw `card_benefit.card_benefit_id` |
| `remaining_value` | dollar or qualitative value |
| `deadline` | expiration or reset |
| `workflow_name` | executable reference or workflow name |
| `required_user_actions` | login, payment, confirmation, upload, etc. |
| `expected_cost` | estimated cost |
| `expected_recovery` | expected credit or value |
| `risk_level` | low / medium / high / unknown |
| `risk_notes` | concise notes |
| `source_confidence` | confidence value |

## Post-Action Monitoring

Use this after a benefit action creates a transaction, booking, change, cancellation, enrollment, or redemption.

Evidence priority:

1. Statement credit line item.
2. Issuer benefit tracker.
3. Transaction record.
4. User-provided statement evidence.
5. User confirmation.

Status values:

- `pending`
- `posted`
- `partially_posted`
- `not_posted`
- `reversed`
- `expired`
- `blocked`

Rules:

- Do not mark a benefit as used until credit or usage is verified.
- If a refund occurs before credit posts, continue monitoring.
- If credit posts then reverses, reopen the benefit if issuer tracker evidence supports that conclusion.
- If the period expires, mark residual value as missed or unknown.

## Completion Criteria

The session is complete only when:

- every scoped card is classified as live, closed, blocked, or out of scope
- every scoped benefit is classified as verified, inferred, unknown, or blocked
- every suggested action has a source, amount, deadline, risk, and required user action
- all irreversible actions were explicitly confirmed or left as handoffs
- SQLite state passes `PRAGMA foreign_key_check`
