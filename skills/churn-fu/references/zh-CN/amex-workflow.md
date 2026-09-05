# Amex 工作流

这是当前版本第一个支持的 issuer adapter。

## 范围

- 支持 issuer：Amex。
- 支持任务：卡片 inventory、benefit catalog discovery、usage status audit、enrollment status、statement credit monitoring。
- 当前不支持：自动输入密码、CardPointers enrichment、非 Amex issuer。

## 登录

1. 打开 portal 前先读取 `login-flows.md`，并遵循其中的 American Express 小节。
2. 只有用户允许 portal handoff 时才打开 Amex portal。
3. 登录后，只把选中的 Amex login 当作 runtime login label，除非用户提供其他非敏感 PointClaw owner label。
4. 通过 portal 可见状态或用户确认来验证账号上下文。

## 卡片 inventory

对每张可见卡：

- 匹配或分配 PointClaw `card_instance.card_id`。
- public product name 写入 `card_product.product_name`。
- portal 可见的 card last four 写入 `card_instance.last_digits`。
- lifecycle state 写入 `card_instance.card_state`。
- 不要把 product name 当唯一标识。同名产品用 `card_instance.card_id` 区分；如果可见，再结合 `card_instance.last_digits`。

## 福利 catalog

source order：

1. Amex 官方 product terms 和 benefit guides。
2. 登录后的 Amex benefit pages，用于 account-specific 或 cardmember-only terms。

当前版本不启用 CardPointers enrichment。

## 使用状态

usage status 可来自：

- Amex benefit tracker
- statement credit
- transaction plus credit evidence
- user confirmation

public terms 只能定义福利，不证明 used 或 remaining amount。

当前周期 usage 写入 PointClaw `benefit_status_snapshot`，并通过 `card_benefit.card_benefit_id` 关联；每次 evidence pass 写入 `capture_run`。
