---
name: macos-disk-cleanup
description: 安全扫描并清理 macOS 开发机磁盘空间。适用于 Xcode、Simulator、/private/tmp PR 产物、Homebrew 与开发缓存；可在每天首次登录时触发只读扫描与清理提案，并要求实时预检、精确目标冻结、用户确认、可审计删除与回收验证。
---

# macOS Disk Cleanup

用于“扫整台 Mac 磁盘”“找增长最快/最占空间目录”“清理 Xcode、Simulator、临时测试产物”等请求。

目标是回收空间，而不是泛化地删除“旧文件”。每次执行都必须把：

1. 当前占用与候选范围；
2. 是否为可再生成产物；
3. 是否被当前进程或当前设备使用；
4. 删除会失去什么，以及是否能恢复；
5. 精确删除目标与删除后的验证

分开证明。

## 不变原则

- 历史扫描、截图、磁盘大小和设备状态都只作线索；删除前必须重新扫描。
- 默认只扫描；先向用户说明清理方向、风险和预计空间，得到确认后才删除。
- 不用宽泛 glob、rm -rf、find ... -delete 或直接删一个大父目录。
- 永远不因为目录名像 cache 就删。先证明确实是可再生成物、范围正确、未占用。
- 每个删除目标必须是绝对路径或精确 UDID；删除后必须验证目标已消失、保留项仍在。
- APFS 的逻辑目录大小不等于立刻可回收的物理空间；最终以 df -H /System/Volumes/Data 为准。
- 没有两次或以上可比较快照时，只报告当前占用与最后活动时间，不把它说成增长速度。

## 每日首次登录触发器

不设当前可用空间阈值。安装的 LaunchAgent 在每天首次登录时触发一次；它以本地日历日期去重，不会在同一天重复弹窗。扫描仍记录当前 `df`，但空间大小只用于报告，不决定是否执行。

触发后的默认行为：

1. 重新执行“建立实时基线”，并写一份带时间戳的只读报告；
2. 按本技能的排除项和类别策略提出候选，附带预计逻辑大小、占用情况与风险；
3. 计算满足“每日确认后的立即删除规则”的候选逻辑总大小。若少于 50 GB（50,000,000,000 bytes，即 48,828,125 KiB），只保留报告和日志、不通知、不删除，等待下一天重新扫描；达到或超过该值才通知用户“每日清理计划已就绪，等待确认”；
4. 不把每日触发当作删除授权。没有当次或预先写明的精确 standing authorization 时，自动化不得删除任何目录、Simulator、Device Support 或应用数据。

允许的 standing authorization 必须逐类写清：父目录、候选条件、最小年龄/截止日、明确排除项、是否允许删除历史归档，以及失败时只报告还是停止。即使已有 standing authorization，每轮仍要做 lsof、mtime、路径边界、目标冻结和删除后验证；任何预检不一致都 fail closed。

默认不允许自动删除的类别：/private/tmp PR 产物、Device Support、任何 Simulator、CoreDevice/应用数据、归档与未分类文件。它们分别依赖远端 PR 状态、当前实体设备版本、simctl 注册状态或恢复价值，必须每次单独批准。

### 每日确认后的立即删除规则

“立即删除”只表示：每日首次登录触发后，用户已看过只读报告并在原生 macOS 对话框明确选择“Delete Now”时，不再需要第二轮对话即可执行。它不是后台静默删除授权。

首版 standing authorization **只** 覆盖 `~/Library/Developer/Xcode/DerivedData` 的顶层项目构建目录，且所有条件必须同时成立：

1. 整棵目录在过去 7 个完整自然日内没有任何改动；
2. 无 `lsof` 打开的文件，目录不是 symlink，且目录内深度 3 不含 `.git`；
3. 不属于共享缓存：`ModuleCache.noindex`、`CompilationCache.noindex`、`SDKStatCaches.noindex`、`SymbolCache.noindex`；
4. 删除前立即重新检查路径边界、mtime、大小和占用，冻结为当天审计清单；
5. 不设可删除容量上限；但遇到任何预检不一致或命令失败即停止，保留其余候选。

在上述用户确认后，合格项目目录应立刻逐项删除和验证；仍须记录删除前后 `df`。不得把这条规则扩展到 `/private/tmp`、Device Support、Simulator、CoreDevice、应用数据、archives 或任何未分类内容。以后若想扩大自动执行范围，必须先单独修订此规则并由用户明确确认。

每日通知门槛由 wrapper 在 Codex 只读扫描后自行重新计算：仅汇总当前仍满足本规则的 `DerivedData/TadaWords-*` 顶层目录，逐项检查 7 天整树无活动、非 symlink、无 `.git`、无打开文件描述符并排除共享缓存。该逻辑总大小不等同 APFS 实际可回收物理空间；本地预检不一致时，自动化必须 fail closed：记录错误、不通知、不删除，次日重新扫描。

每次用户确认删除后，自动化必须追加一条不可覆盖的 metrics 记录：确认时的候选逻辑 KiB、删除前后数据卷可用 KiB、实际可用空间差值、Codex 退出状态、删除报告路径，以及从删除报告取得的已删目标数和逻辑 KiB。删除报告首三行必须分别是 `DELETED_TARGET_COUNT: <非负整数>`、`DELETED_LOGICAL_KIB: <非负整数>` 与 `DELETION_STATUS: <completed|stopped|failed>`；实际物理空间指标以 wrapper 的 `df` 前后测量为权威。

## 绝对排除项

除非用户点名并单独确认，以下只报告、绝不自动清理：

- 用户应用数据：~/Library/Application Support、~/Library/Containers 中的 Claude、Notion、Google、浏览器、同步盘、聊天、照片和文档数据。
- .codex、代码仓库、worktree、未提交工作、签名材料、备份和恢复目录。
- CoreDeviceService、连接物理设备的 app/container 数据，以及仍在使用的 TestFlight/归档证据。
- 已注册 Simulator 的内部目录；不得直接删除 ~/Library/Developer/CoreSimulator/Devices/<UDID>。
- 正在 Booted 的 Simulator、命名为 Demo/QA/当前发布验证的设备，除非用户明确点名。
- 当前连接的实体设备所对应的当前 iOS/iPadOS 版本支持包。

## 工作流

### 1. 建立实时基线（只读）

先获取卷级空间和一级候选。优先使用 rg 查找已知清理记录，避免把旧记录当现状。

    df -H /System/Volumes/Data
    du -sk ~/Library/Developer /private/tmp ~/Library/Caches 2>/dev/null
    du -sk ~/Library/Developer/Xcode/DerivedData ~/Library/Developer/CoreSimulator/Devices ~/Library/Developer/Xcode/iOS\ DeviceSupport 2>/dev/null

对大目录向下展开到能够解释“谁在占空间”的粒度。报告应区分：

| 类别 | 典型内容 | 默认动作 |
|---|---|---|
| 可再生成开发产物 | DerivedData、.xcresult、临时 .xcarchive、临时 build 目录 | 预检后可建议删除 |
| 版本支持缓存 | iOS Device Support | 对照当前实体设备版本后建议删除旧版本 |
| Simulator | 注册设备、unavailable、orphan | 只经 simctl 管理 |
| 真实应用/设备数据 | CoreDevice、App Support、Containers | 报告，默认保留 |
| 通用包缓存 | Homebrew、npm、uv | 使用各自的官方 cleanup；先 dry-run |
| 未分类大文件 | archives、VM、下载、同步盘 | 只列出，等用户决定 |

### 2. 先说明清理方向，再拿确认

在任何破坏性动作之前，用简短中文说明：

- 将处理的类别、截止日期/状态条件和预计大小；
- 保留的类别；
- 是否会丢失本地 App 数据、Simulator 测试状态或历史归档；
- 哪些内容可重新下载/重建，哪些不能字节级恢复。

确认必须与实际范围匹配：

- “第一批”只授权当时列出的类别和精确条件。
- “所有已合并 PR”不包含已关闭未合并 PR。
- “所有 closed PR”才包含 closed-unmerged PR；远端状态仍要实时核验。
- “删旧 Device Support”只授权确认过的旧系统版本，不授权删除同设备型号的当前版本。

### 3. 对每类候选执行专用预检

通用预检（每个即将删除的目标）：

1. 确认路径存在、是目录而非 symlink，且落在批准的父目录内。
2. 记录 du -sk、根目录 mtime（stat -f '%m'）和绝对路径。
3. 以 lsof -nP 检查目标或其子路径是否有打开的文件描述符。
4. 冻结为 TSV/Markdown 审计清单，再次比较大小与 mtime；任何变化或占用都中止该批。
5. 先写清恢复边界，再删除。

审计记录默认放在：

    ~/Documents/Codex/disk-cleanup-records/

记录应包含：时间、用户授权语义、候选条件、精确清单、预检结果、执行结果、保留项、df 前后读数和恢复边界。不要记录凭据、签名 URL 或私密 App 内容。

## 类别策略

### A. /private/tmp 的 TadaWords / PR 生成物

适用内容：带 PR 号的 .xcresult、.xcarchive、Derived、simulator build、release-export、临时测试目录。

选择规则：

1. 只考虑 /private/tmp 的顶层目录；不递归从整个 /private/tmp 猜测删除目标。
2. 从目录名提取 PR 号（例如 pr112）；通过远端 GitHub 查询每个 PR 的实时 state 与 merged。
3. 仅选取用户授权的状态（merged 或 closed）。没有可验证 PR 号、名称含混、或对应 open PR 的目录一律保留。
4. 在目标中检查 .git（至少到深度 3）；若发现 Git 元数据，按工作树处理，停止自动删除。
5. 检查全局 lsof 是否仍引用目标。没有占用、目录静态、且是顶层临时产物后，才可删除。

注意：

- 合并后的历史 archive/test evidence 通常可从源重新构建，但不能字节级重建。删除前明确写入审计记录。
- 对 closed-unmerged PR 的删除必须来自用户“所有 closed”的明确授权，不能从“已 merge”推断。

删除时从冻结 TSV 中逐行读取绝对路径；逐项删除并立刻确认路径不存在。绝不删除 /private/tmp 本身，也不使用一个模式同时删除未在清单中的目录。

### B. Xcode DerivedData

适用内容：~/Library/Developer/Xcode/DerivedData 下的顶层构建缓存。

选择规则：

1. 用户给出截止日时，检查整个目录树是否存在在截止日或之后改动的项；不能只看根目录 mtime。
2. 保留任何有新内容、正在被 Xcode/xcodebuild 使用、或位于当前构建/测试活动中的目录。
3. ModuleCache.noindex、CompilationCache.noindex、SDKStatCaches.noindex 等共享缓存只有在同一“全树截止日 + 无占用”规则通过时才可删除；否则保留。
4. SymbolCache.noindex 可按相同规则处理；在报告中单列，避免把它误当项目 DerivedData。

示例判断：

    find "$candidate" -newermt 'YYYY-MM-DD 00:00:00' -print -quit

输出为空才表示目录树没有晚于截止日的内容。冻结清单后再跑一次同样检查和 lsof。

恢复边界：会触发下次 Xcode 构建重新索引、下载或编译；不会删除源代码，但会删除本地构建和测试产物。

### C. iOS Device Support

路径：~/Library/Developer/Xcode/iOS DeviceSupport

选择规则：

1. 通过 xcrun devicectl list devices 或 xcrun xcdevice list 实时取得已配对实体设备的 modelCode 和 operatingSystemVersion。
2. 只考虑“同型号、旧系统 build”的支持包；保留当前实体设备系统版本的包。
3. 明确区分：设备型号可能仍是正在使用的物理设备；删除的是旧 iOS/iPadOS 调试支持缓存，不是设备、App、设备数据或 Simulator runtime。
4. 优先使用 System Settings → General → Storage → Developer → iOS Device Support 删除。
5. 如果系统界面不列出目标、不可访问或明显陈旧：
   - 不可盲选当前可见行；
   - 重新确认精确路径、当前设备系统版本和无占用；
   - 只有用户明确授权“按这两个精确路径直接删”后才可改为直接路径删除。

恢复边界：旧版本设备重新连接时，Xcode 可重新下载支持包；不能把同型号当前系统版本包一起删。

### D. CoreSimulator

路径：~/Library/Developer/CoreSimulator/Devices

必须遵守：

- 使用 xcrun simctl list devices -j 作为注册状态权威来源。
- 删设备只能用 xcrun simctl delete <UDID>，不得直接删除 Devices/<UDID>。
- unavailable / orphan 是高优先级候选；registered 不等于可自动删。
- “全部 Shutdown 设备”会永久丢失每台 Simulator 的 App、数据库、登录、媒体、截图和测试状态；需用户明确授权这个范围。
- 即使用户授权批量 Shutdown，也要冻结每个 UDID、名称、runtime、状态和大小，保留 Booted/命名 Demo/QA/当前验证设备。
- 删除后同时验证：
  1. UDID 已从 simctl list devices -j 消失；
  2. 匹配 Devices/<UDID> 目录已消失；
  3. 保留设备仍注册/Booted。

不要把“目录很大”或“状态 Shutdown”本身当作删除授权。

### E. Homebrew、npm、uv

- Homebrew：先 brew cleanup --dry-run --prune=all，报告项目数和大小；用户确认后执行 brew cleanup --prune=all。
- npm / uv：优先使用各自支持的缓存清理命令和 dry-run；没有可靠 dry-run 时只报告，除非用户明确批准。
- 在执行前确认没有对应的 brew/npm/npx/uv 构建或下载进程。

## 删除执行与后验验证

删除执行器必须：

1. 从冻结清单逐行读取；
2. 每一项在删除前再次检查大小、mtime、边界和占用；
3. 条件不匹配则 fail closed：停止该批，不删除变化中的目标；
4. 只对已授权的精确路径使用非 glob 的递归删除；
5. 每项删除后验证路径/UDID 不存在；
6. 最后重新执行 df -H /System/Volumes/Data 并报告实际可用空间变化。

若 GUI 的最终 Delete/永久删除按钮被自动化驱动，必须在点击前进行即时确认；不把较早的泛化确认当成该最终按钮确认。

## 最终交接格式

用以下顺序汇报：

1. 实际删除了什么：数量、类别、逻辑大小；
2. 物理空间结果：df 前后、当前可用空间；
3. 保留了什么：应用数据、CoreDevice、当前 Device Support、Booted/命名 Simulator；
4. 未执行项和原因：例如 UI 未列出目标、占用、状态变化或缺少确认；
5. 审计记录路径与恢复边界。

不要把“候选”写成“已删除”，不要把目录逻辑大小写成实际释放空间。
