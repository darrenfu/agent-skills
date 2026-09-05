# MCP 安装策略

当缺少本地依赖，例如 `sqlite3`，使用本文件。

## 策略

1. 不要静默安装系统软件。
2. 优先使用可信第三方 installer 或 package-manager MCP。
3. 搜索当前可用工具中是否有 installer/package-manager 能力。
4. 如果存在合适 MCP，说明要安装的依赖和原因，并在调用前获得用户批准。
5. 如果没有合适 MCP，询问用户是否需要手动安装路径。
6. 数据库存在后，把 blocker 记录到 SQLite；数据库尚未创建前，先记录在 session blocker list。

## sqlite3 缺失时的措辞

```text
Churn Fu 需要 sqlite3 来初始化本地状态。我没有找到可用的 sqlite3 命令。如果当前环境配置了 installer/package-manager MCP，我会在你批准后使用它；否则需要你批准我提供或执行本机的手动安装路径。
```

## 禁止事项

- 不要未经用户批准运行 package manager 命令。
- 不要凭猜测选择 package manager。
- 不要安装无关依赖。
- 不要绕开 SQLite 改用隐藏的其他数据库引擎。
