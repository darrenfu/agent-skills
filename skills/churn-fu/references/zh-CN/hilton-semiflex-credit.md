# Hilton Semi-Flex Credit 工作流

用于 Amex Hilton Aspire、Surpass、Business Platinum Hilton statement credit 的 Hilton semi-flex 预订与后续退款流程。该流程只在用户明确要求执行时使用；live run 第一次 Hilton submit 前，必须获取覆盖 eligible booking/refund/cancellation scope 的 site-level batch authorization。

## 触发条件

- SQLite/Amex tracker 显示当前 half 或 quarter 仍有 Hilton 类福利未使用。
- 用户接受论坛 DP 风险：Hilton credit 可能延迟、失败，退款后也可能 reverse。
- 目标是先创建可取消的 Hilton direct charge，并把福利状态记为 `pending_credit`，不是直接记为完成。

## 总流程

1. 查 Amex Hilton 系列卡的未使用福利。
2. 按卡产品分流：
   - Aspire：Hilton Resort Credit，按 half-year 使用。
   - Surpass：Hilton Credit，按 quarter 使用。
   - Business Platinum：Hilton Statement Credit，按 quarter 使用。
3. 到 Hilton 官网检查已登录状态；如果没有登录，停下让用户完成 saved login。
4. 预订 `Hilton Grand Vacations Club Flamingo Las Vegas`。
5. 订 8 months 之后、非旺季、非节假日周末、1 night。
6. 选最便宜的 `Honors Discount Semi-Flex`；每晚房价必须低于 $300。
7. 如果目标日期不满足价格或 availability，往后 roll 1 个月，最多试 5 个 date；仍找不到则退出报错。
8. Payment 页面点 Edit card，按目标 card alias 匹配 saved card 的 last four 和 expiry。
9. 如果 saved card last four 有 duplicates，必须用 expiry 消歧；仍不唯一时停止让用户手动选。
10. 第一次 final booking submit 前，验证或请求 site-level batch authorization，覆盖 Hilton、eligible cards、card last four/expiry scope、benefits、room price ceiling、taxes/fees ceiling、stay date window 和 cancellation rule。
11. active site-level batch authorization 有效时提交每个 covered booking；不要按卡或 reservation 逐笔确认。
12. 提交成功后记录 reservation alias、可见 confirmation、hotel、date、rate、total、card last four、expiry、福利周期，状态记为 `pending_credit`。
13. Do not schedule cancellation until all target bookings are complete.
14. 全部订完后，不按固定天数 refund；必须先登录 Amex 并确认 Amex credit statement 到账，才启动 refund 流程。refund/cancellation submit 需要当前 live run 有 active Hilton site-level batch authorization。

## 日期和价格规则

- 默认从当前日期所在月往后 8 months，取目标月份第一个周三；下一个尝试日期为后续月份第一个周三。
- 最多尝试 5 个日期。
- 避开节假日、长周末、大型活动高峰；如果页面价格明显偏离，继续 roll。
- 房型选择最低价 semi-flex，优先 `Honors Discount Semi-Flex`。
- 每晚房价必须小于 $300，不包含 taxes/fees；如果只有更贵价格，换日期。

## 浏览器和登录规则

- 先读取 `login-flows.md`；booking 登录按 Hilton 小节执行，credit 到账检查按 American Express 小节执行。
- 每次新订单第一步先检查 Hilton 是否已登录；未登录则先 sign in。
- 只使用可见 saved login/autofill；不读取任何 secret。
- 页面卡住超过 60 seconds 时，直接 close 当前 booking flow page，重新从 Hilton 搜索页开始。
- 遇到额外身份验证、支付验证、页面异常或订单状态不明确，停止并让用户接管。

## 确认范围

按 `safety-confirmations.md` 使用 site-level batch authorization。同一 live run 中，只要 site、account、hotel、date-window strategy、room-rate ceiling、card/payment mapping、cancellation rule 和 risk envelope 不变，一次 Hilton 确认可覆盖所有 eligible bookings。

如果 site、account、hotel、amount ceiling、payment mapping、date-window strategy、cancellation/refund terms 或 material risk 变化，必须重新确认。

## Payment 方法

- 只使用 saved card，优先匹配 PointClaw card alias 对应的 visible last four。
- 同一个 last four 出现多张 saved card 时，用 expiry 区分。
- 如果 last four + expiry 仍无法唯一匹配，必须 ask for manual selection。
- 不记录完整卡号或其他 secret；DB 只记录 last four、expiry、card alias、benefit alias 和 reservation alias。

## DB 状态

每个成功 booking 后：

- 写入当前 period 的 PointClaw snapshot：
  - Aspire: `semiannual`, 如 `2026-H2`, limit $200。
  - Surpass / Business Platinum Hilton: `quarterly`, 如 `2026-Q3`, limit $50。
  - `status_code`: `pending_credit`。
  - `used_amount_cents`: 福利 cap。
  - `remaining_amount_cents`: 0。
- 写入 redemption attempt，`action_state` 用 `submitted`。
- 写入 manual note，包含 reservation alias、hotel、rate、date、total、last four、expiry 和 Amex statement credit 检查 cadence。
- 不要仅因 charge 成功就标记为 issuer credit posted；Amex tracker 或 statement credit evidence 出现后才升级为 completed/used evidence。

## Amex credit statement 到账后 refund

统一安排在全部 booking 完成后监控：

1. 每 7 days 登录并检查所有已订房但还没 refund 的 Amex 卡。
2. 检查 Amex statement credit 是否已到账；可接受 evidence 包括 statement credit transaction、benefit tracker 明确扣减，或同等 Amex portal evidence。
3. 只要某张卡的 Amex statement credit 已到账，就可以为该 reservation 启动 refund 流程。
4. 如果某张卡 booking 后超过 21 days 仍没有 Amex credit 到账，report error 给用户；不要自动 refund。
5. 对未到账且未超过 21 days 的卡，保持 `pending_credit` 并等下一次 7 days check。

启动 refund 后：

1. 打开 Hilton reservation。
2. 验证 hotel、date、rate、refund/cancellation policy、refund destination 和 refund amount。
3. 如果页面显示 non-refundable、partial refund、refund method 不明确，停止询问用户。
4. final cancellation/refund 前，验证 active site-level batch authorization 覆盖 reservation alias scope、refund amount、refund method 和 credit reversal 风险。
5. active site-level batch authorization 覆盖 final refund/cancellation details 时才执行。
6. 执行后记录 cancellation attempt；继续监控 Amex credit 是否 reverse。

## Dry Run / Eval

使用：

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py hilton-semiflex-dry-run --as-of YYYY-MM-DD
```

Dry run 必须只使用 mock state，不打开 live Hilton、Amex、Chrome 或网络页面。它验证 eligible benefits 数量、日期 roll 策略、last four + expiry 消歧、60 seconds 卡住恢复策略、7 days Amex check cadence、21 days report error threshold 和 `pending_credit` 状态。
