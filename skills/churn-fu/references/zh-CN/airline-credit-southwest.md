# Airline Credit Southwest 工作流

只有当 SQLite 中存在 ready airline credit action candidate 时使用。

## 前置条件

- Benefit usage 显示当前周期有 remaining value，或用户接受不确定性。
- Payment method alias 已映射到 card alias。
- Travel workflows 已启用。
- Execution mode 是 `user-confirmed-execution`。
- Chrome 可用于 airline site，或用户准备手动完成登录。
- 用户理解 issuer credit 可能延迟 post，也可能在退款后 reverse。

## 凭证默认策略

先读取 `login-flows.md`，并按其中 Southwest 小节处理 Chrome autofill 和 login handoff。

1. 在 Chrome 打开 airline site。
2. 只使用 `login-flows.md` 描述的、用户批准的可见 Chrome password-manager 路径。
3. 不读取 password、cookie、token、local storage 或 password database secret fields。
4. 遇到 MFA、CAPTCHA、passkey、identity verification 或 payment verification，停止并交给用户。
5. 如果 autofill 不可用，要求用户手动登录并在完成后告知。

## 默认路线和日期策略

默认搜索路线：

- `HNL -> OGG`
- 将其视为匿名化的操作默认值：一条 Honolulu-origin 的短 Southwest route，通常有低价、可改签选项。

如果该路线不可用或价格不合适，记录失败原因后再改用其他低价 Southwest route。

默认日期规则：

- 选择当前日期约 5 个月后的日期。
- 避开 Thanksgiving week。
- 避开 Christmas 到 New Year。
- 避开 major holiday weekends。
- 避开 major holidays 相邻日期。
- 避开离当前日期过近的日期。

## 金额追踪模型

预订前计算：

- `target_remaining_credit`: SQLite 中当前周期 remaining benefit amount。
- `target_card_id`: benefit 绑定的 PointClaw `card_instance.card_id`。
- `target_card_benefit_id`: PointClaw `card_benefit.card_benefit_id`。
- `payment_method_alias`: airline saved payment alias，必须映射到 PointClaw card id 或 visible last four。
- `cumulative_candidate_charges`: 本 workflow 中 purchase 和 change charge 的累计值。
- `remaining_gap`: `target_remaining_credit - cumulative_candidate_charges`。

每次确认 purchase 或 change 后：

1. 在 session output 中记录 action；只有 PointClaw 有对应 workflow table 时才持久化。
2. 重新计算 `cumulative_candidate_charges`。
3. 如果 `cumulative_candidate_charges >= target_remaining_credit`，退出 purchase/change loop。
4. 如果仍低于 target，进入 change flow，寻找合理追加金额；经验偏好是每笔改签 charge 尽量接近 `$70`。

不要因为 charge 已发生就把 benefit 标记为 used。必须先标记为 `pending_credit`，直到 issuer evidence 验证 credit 或 usage tracker 更新。

## Fare 可退款规则

Southwest workflow 默认目标是创建可全额退回原支付方式的现金票，不是创建未来 flight credit。

- 只允许选择 Southwest 官方标记为 refundable 的 fare：`Choice Preferred` 或 `Choice Extra`。
- 禁止选择 `Basic` 或 `Choice`，即使价格更低、可取消、可改签或可产生 flight credit。
- 不要把 `cancellable`、`changeable`、`transferable flight credit` 或 `no cancel fees` 当成 `refund to original form of payment`。
- 如果现有 reservation 的任一资金来源来自 `Basic`、`Choice`、flight credit、voucher、gift card 或其他非现金可退来源，不得假设后续升级到 refundable fare 会把这部分变成可退回原卡。
- 订票、改签和取消前都要核对每一部分金额的 refund destination；只要任何部分会进入 flight credit、travel credit、voucher 或不明确状态，就必须停止并询问用户。

## 流程

## 确认范围

live run 中第一次 Southwest transaction submit 前，按 `safety-confirmations.md` 获取 site-level batch authorization。授权必须覆盖 airline site、account、eligible reservation/card/payment scope、per-transaction cap、total batch cap、route/date/fare constraints、refundability requirement 和 issuer-credit reversal risk。

之后，只要 purchase、change 或 cancellation 仍在已确认的 Southwest envelope 内，不要按 card 或 reservation 逐笔确认。只有 site、account、amount ceiling、payment mapping、route/date/fare rules、refundability 或 risk envelope 变化时才重新确认。

### 1. 读取 candidate

1. 从 SQLite 查询 open airline credit candidate。
2. 验证 benefit type 是 airline credit 或等价类型。
3. 验证 usage status 和 remaining amount。
4. 验证 payment method alias 映射到 candidate PointClaw `card_instance.card_id` 或 visible last four。
5. 如果映射缺失或模糊，停止并要求用户把 airline saved payment method 映射到 card。

### 2. Airline 登录

1. 在 Chrome 打开 Southwest 或配置的 airline site。
2. 尝试用 Chrome autofill 登录 saved airline account。
3. 如果登录表单需要用户操作，handoff 给用户完成 login/MFA 并等待。
4. 登录后通过可见账号身份或用户确认验证 account context。

### 3. 初始预订

1. 默认搜索 `HNL -> OGG`。
2. 使用约 5 个月后的日期，并避开 holiday windows。
3. 只选择 `Choice Preferred` 或 `Choice Extra`；如果只有 `Basic` 或 `Choice` 价格合适，停止并报告没有合规 refundable 选项。
4. 在页面或官方 fare text 中验证该 fare 支持 refund to original form of payment。
5. 避免 optional paid add-ons。
6. Decline credit-card ads、promotional financing offers 或 upsells。未经用户确认，不接受付费 add-ons。
7. 选择映射到 target card alias 的 saved payment method alias。
8. 最终 purchase/review 前，验证 active site-level batch authorization 覆盖本次 purchase；否则停止并请求授权。
9. site-level batch authorization 必须包含：
   - card alias
   - payment method alias
   - per-transaction amount 和 total batch ceiling
   - route
   - date window
   - flight time
   - fare type
   - refundability: 必须明确为 refund to original form of payment
   - target remaining credit
   - purchase 后 expected cumulative charges
10. active site-level batch authorization 覆盖 final review details 时才 purchase。
11. 记录 reservation alias、charge amount、route、date、fare type、refundability、payment method alias 和 `submitted` 状态。

### 4. 检查是否覆盖目标

1. 重新计算 `cumulative_candidate_charges`。
2. 如果累计 charge 已达到或超过 `target_remaining_credit`，停止新增 charge。
3. 如果累计 charge 低于 target，计算 `remaining_gap`。
4. 只有用户仍希望继续覆盖 remaining gap 时才进入 change flow。

### 5. Change / Fare Difference Loop

重复直到累计 charge 达标或用户停止：

1. 打开 reservation change flow。
2. 必要时搜索同路线/同日期或附近 eligible itinerary。
3. 只选择 `Choice Preferred` 或 `Choice Extra`；禁止改到 `Basic` 或 `Choice`。
4. 每笔改签优先选择接近 `$70` 的 additional fare difference，但 refundability 优先级高于价格目标。
5. 如果多个 refundable 选项都接近 `$70`，选择最能覆盖 `remaining_gap` 且 overage 最小的选项。
6. 避免大额 overage，除非用户明确接受。
7. final change confirmation 前，验证 active site-level batch authorization 覆盖本次 change；否则停止并请求新授权。
8. site-level batch authorization 必须覆盖：
   - reservation alias
   - additional amount due
   - 与 `$70` per-change target 的差距
   - new cumulative candidate charges
   - change 后 remaining gap
   - route/date/flight/fare type
   - refundability: 必须明确为 refund to original form of payment；如果 reservation 含历史 non-refundable funds，要单独列出这部分风险
   - payment method alias
   - issuer credit 不 post 或 reverse 的风险
9. active site-level batch authorization 覆盖 final change details 时才 confirm change。
10. 在 session output 中记录 change；只有 PointClaw 有对应 workflow table 时才持久化。
11. 重新计算 `cumulative_candidate_charges`。
12. 如果 target 已满足，退出 loop。

### 6. 退出条件

以下任一条件成立即退出 booking/change loop：

- `cumulative_candidate_charges >= target_remaining_credit`
- 没有合理低 overage change
- payment method mapping 变得模糊
- 用户拒绝继续 charge
- airline site 阻塞流程
- 到达 final side-effect step 但没有 active site-level batch authorization

### 7. 安排取消

如果创建了可取消 reservation：

1. 除非用户指定其他时间，否则安排次日 11:00，使用配置/系统时区。
2. 存储：
   - reservation alias
   - route
   - date
   - fare type
   - total candidate charges
   - expected refund method: full refund to original form of payment
   - non-refundable funds check: none expected
   - stop before final cancellation 的指令
3. 声称 scheduled 前必须验证 timezone handling。

### 8. 取消 / 退款

到取消时间：

1. 打开 airline cancellation flow。
2. 通过 alias 或用户提供的 confirmation 找到 reservation。
3. 验证 passenger alias、route、date、fare type、refund method、refund amount。
4. refund method 必须是全额 refund to original form of payment。
5. 如果网站只提供 travel credit、flight credit、voucher、points redeposit，或只有部分金额 refund to original form of payment，必须停止并询问用户。不要取消。
6. final cancellation 前，验证 active site-level batch authorization 覆盖本次 cancellation；否则停止并请求新授权。
7. site-level batch authorization 必须覆盖：
   - reservation alias
   - route/date
   - refund amount
   - refund method: full original form of payment
   - flight credit amount: 必须为 `$0` 或 none
   - issuer credit reversal 风险
8. active site-level batch authorization 覆盖 final cancellation details 时才 cancel。
9. 在 session output 中记录 cancellation 和 refund request；只有 PointClaw 有对应 workflow table 时才持久化。
10. 继续监控 issuer credit posting 和 reversal status。

## 风险

Issuer credit 可能延迟 post，也可能在 refund 后 reverse。不要把 pending credit 标记成 completed usage。
