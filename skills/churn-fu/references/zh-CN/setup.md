# 设置流程

第一次使用 Churn Fu 时使用本文件。

## 流程

1. 定位 `<PLUGIN_ROOT>`。
2. 运行环境检查：

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py doctor
```

3. 如果缺少 `sqlite3`，使用 `mcp-installer-policy.md`。依赖安装优先通过可信的第三方 installer/package-manager MCP，并且必须获得用户批准。
4. 读取 `first-run-config.md`。
5. 不询问冗长配置，直接生成默认配置：

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py config-wizard
```

6. 初始化数据库：

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py init-db
```

7. 校验：

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py validate
```

8. 查看状态：

```bash
python3 <PLUGIN_ROOT>/scripts/churnfu.py status
```

默认配置位于 `<PLUGIN_ROOT>/skills/churn-fu/local/`。默认数据库是 `<PLUGIN_ROOT>/../pointclaw-data/pointclaw.sqlite`；历史 Churn Fu local database 只作为 legacy/BC 使用。

## 当前版本范围

- 只支持 Amex。
- 暂不启用 CardPointers enrichment。
- 状态源是 PointClaw SQLite。
- 默认数据库：`../pointclaw-data/pointclaw.sqlite`。
- Legacy 数据库：skill 的 `local/` 目录，仅用于 BC 读取或 legacy benefit sync。
- 登录策略：优先使用 Chrome saved-password autofill，MFA/OTP/CAPTCHA/CVV 等敏感步骤由用户处理。
- 所有 purchase / change / cancel / booking / enroll / redeem 都必须用户最终确认。
