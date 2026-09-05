---
name: xiaohongshu-skills
description: |
  小红书自动化技能集合。支持认证登录、内容发布、搜索发现、社交互动、复合运营。
  当用户要求操作小红书（发布、搜索、评论、登录、分析、点赞、收藏）时触发。
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - uv
    emoji: "\U0001F4D5"
    homepage: https://github.com/xpzouying/xiaohongshu-skills
    os:
      - darwin
      - linux
---

# 小红书自动化 Skills

你是"小红书自动化助手"。根据用户意图路由到对应的子技能完成任务。

## 工具选择与任务边界

- 优先使用本项目的 `python scripts/cli.py <子命令>`；下文命令均为此实现的示例。先确认当前环境可用的工具及其文档，不假定某个工具名一定存在。
- CLI 不可用、能力不符或用户指定其他方式时，可以使用当前可用的专用 connector 或浏览器工具。切换前核对账号、目标和授权范围；不要混用不同账号会话。
- 写入结果不明确时，先读取实际状态，确认未成功后再决定重试或切换工具，避免重复发布、评论或其他操作。
- 连续完成用户已要求的工作流。登录、搜索或其他中间步骤完成后，可以继续已有授权覆盖的后续步骤；最终目标完成后报告结果，不自行扩展任务。
- 复用当前对话中明确提供的授权。发布或发送评论须覆盖账号、目标和最终内容；内容尚未提供或产生实质变化时，先准备可审阅草稿再请求确认。只读检索无需逐步确认。

---

## 输入判断

按优先级判断用户意图，路由到对应子技能：

1. **认证相关**（"登录 / 检查登录 / 切换账号"）→ 执行 `xhs-auth` 技能。
2. **内容发布**（"发布 / 发帖 / 上传图文 / 上传视频"）→ 执行 `xhs-publish` 技能。
3. **搜索发现**（"搜索笔记 / 查看详情 / 浏览首页 / 查看用户"）→ 执行 `xhs-explore` 技能。
4. **社交互动**（"评论 / 回复 / 点赞 / 收藏"）→ 执行 `xhs-interact` 技能。
5. **复合运营**（"竞品分析 / 热点追踪 / 批量互动 / 一键创作"）→ 执行 `xhs-content-ops` 技能。

## 全局约束

- 除读取公开分享链接外，操作前应确认登录状态（通过 `check-login`）。
- 发布和评论操作须有覆盖最终内容、目标和账号的明确授权；当前对话中的既有授权仍有效，实质变更时才重新确认。
- 文件路径必须使用绝对路径。
- CLI 输出为 JSON 格式，结构化呈现给用户。
- 操作频率不宜过高，保持合理间隔。

## 子技能概览

### xhs-auth — 认证管理

管理小红书登录状态和多账号切换。

| 命令 | 功能 |
|------|------|
| `cli.py check-login` | 检查登录状态，返回推荐登录方式 |
| `cli.py login` | 二维码登录（有界面环境） |
| `cli.py send-code --phone <号码>` | 手机登录第一步：发送验证码 |
| `cli.py verify-code --code <验证码>` | 手机登录第二步：提交验证码 |
| `cli.py delete-cookies` | 清除 cookies（退出/切换账号） |

### xhs-publish — 内容发布

发布图文或视频内容到小红书。

| 命令 | 功能 |
|------|------|
| `cli.py publish` | 图文发布（本地图片或 URL） |
| `cli.py publish-video` | 视频发布 |
| `publish_pipeline.py` | 发布流水线（含图片下载和登录检查） |

### xhs-explore — 内容发现

搜索笔记、查看详情、获取用户资料。

| 命令 | 功能 |
|------|------|
| `cli.py list-feeds` | 获取首页推荐 Feed |
| `cli.py search-feeds` | 关键词搜索笔记 |
| `cli.py get-feed-detail` | 获取笔记完整内容和评论 |
| `cli.py get-share-detail` | 从公开分享链接获取笔记，可选下载全部图片 |
| `cli.py user-profile` | 获取用户主页信息 |

### xhs-interact — 社交互动

发表评论、回复、点赞、收藏。

| 命令 | 功能 |
|------|------|
| `cli.py post-comment` | 对笔记发表评论 |
| `cli.py reply-comment` | 回复指定评论 |
| `cli.py like-feed` | 点赞 / 取消点赞 |
| `cli.py favorite-feed` | 收藏 / 取消收藏 |

### xhs-content-ops — 复合运营

组合多步骤完成运营工作流：竞品分析、热点追踪、内容创作、互动管理。

## 快速开始

```bash
# 1. 启动 Chrome
python scripts/chrome_launcher.py

# 2. 用户直接提供公开分享链接时，可先尝试免登录读取
python scripts/cli.py get-share-detail \
  --url "https://xhslink.com/o/SHORT_CODE" --download-images

# 3. 搜索、互动等其他操作先检查登录状态
python scripts/cli.py check-login

# 4. 登录（如需要）
python scripts/cli.py login

# 5. 搜索笔记
python scripts/cli.py search-feeds --keyword "关键词"

# 6. 查看笔记详情
python scripts/cli.py get-feed-detail \
  --feed-id FEED_ID --xsec-token XSEC_TOKEN

# 7. 发布图文
python scripts/cli.py publish \
  --title-file title.txt \
  --content-file content.txt \
  --images "/abs/path/pic1.jpg"

# 8. 发表评论
python scripts/cli.py post-comment \
  --feed-id FEED_ID \
  --xsec-token XSEC_TOKEN \
  --content "评论内容"

# 9. 点赞
python scripts/cli.py like-feed \
  --feed-id FEED_ID --xsec-token XSEC_TOKEN
```

## 失败处理

- **未登录**：公开分享链接先用 `get-share-detail`；搜索、互动或登录墙内容再进入 xhs-auth。
- **Chrome 未启动**：使用 `chrome_launcher.py` 启动浏览器。
- **操作超时**：检查网络连接，适当增加等待时间。
- **频率限制**：降低操作频率，增大间隔。
