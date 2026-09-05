# Installed custom skills

Inventory date: 2026-09-05. This catalog covers user-installed or customized skills and excludes Codex built-ins and skills bundled with official plugins.

**50 unique names, 44 packages, and 62 local entrypoint files.** The session advertised 47 names. `banner-design`, `brand`, and `design` were present on disk but absent from that session's advertised list; the reason was not investigated.

Sources: `~/.codex/skills` and `~/.agents/skills`. Duplicate names are consolidated, with complete packages taking precedence. The application-bundled `cua-driver` symlink is materialized as ordinary files. Six nested skills remain inside their `video-use` and `xiaohongshu-skills` parent packages.

The export contains 742 skill and backup files, approximately 25.9 MB, including supporting scripts, templates, references, fonts, and existing example images. See [manifest.json](manifest.json) for exact paths, source aliases, executable permissions, and SHA-256 hashes.

## Finance and daily workflows (6)

| Skill | Purpose | Observed session status |
|---|---|---|
| [churn-fu](../../skills/churn-fu/SKILL.md) | Credit card lifecycle, benefits, and SQLite records | Advertised |
| [costco-vgc-wallet](../../skills/costco-vgc-wallet/SKILL.md) | Staples virtual gift cards, Costco gift cards, and wallet workflows | Advertised |
| [nasdaq-regime-dca](../../skills/nasdaq-regime-dca/SKILL.md) | Nasdaq valuation, drawdowns, and recurring investment strategy | Advertised |
| [stock-risk-first-trading](../../skills/stock-risk-first-trading/SKILL.md) | Risk analysis for stock and options trades | Advertised |
| [paze-restaurant-availability](../../skills/paze-restaurant-availability/SKILL.md) | Find restaurants and verify Paze checkout availability | Advertised |
| [school-calendar-source-finder](../../skills/school-calendar-source-finder/SKILL.md) | Find and verify official school calendars | Advertised |

## Development and operations (8)

| Skill | Purpose | Observed session status |
|---|---|---|
| [cua-driver](../../skills/cua-driver/SKILL.md) | Automate native macOS applications | Advertised |
| [ios-hybrid-delivery](../../skills/ios-hybrid-delivery/SKILL.md) | iOS signing, Xcode Cloud, and TestFlight delivery | Advertised |
| [macos-disk-cleanup](../../skills/macos-disk-cleanup/SKILL.md) | Scan macOS disk usage and perform controlled cleanup | Advertised |
| [stateful-change-delivery](../../skills/stateful-change-delivery/SKILL.md) | Deliver changes involving persistent state, data, and environments | Advertised |
| [vanity-engineering-review](../../skills/vanity-engineering-review/SKILL.md) | Review overengineering and work with limited practical value | Advertised |
| [deploy-to-vercel](../../skills/deploy-to-vercel/SKILL.md) | Deploy applications to Vercel | Advertised |
| [vercel-cli-with-tokens](../../skills/vercel-cli-with-tokens/SKILL.md) | Use the Vercel CLI with token authentication | Advertised |
| [vercel-optimize](../../skills/vercel-optimize/SKILL.md) | Optimize Vercel cost and performance | Advertised |

## Frontend and design (14)

| Skill | Purpose | Observed session status |
|---|---|---|
| [banner-design](../../skills/banner-design/SKILL.md) | Design banners for multiple platforms | Installed on disk only |
| [brand](../../skills/brand/SKILL.md) | Manage brand voice, visual guidelines, and assets | Installed on disk only |
| [design](../../skills/design/SKILL.md) | Create visual designs, logos, icons, and brand materials | Installed on disk only |
| [design-audit](../../skills/design-audit/SKILL.md) | Review UI/UX and produce improvement plans | Advertised |
| [design-system](../../skills/design-system/SKILL.md) | Design tokens, component specifications, and slides | Advertised |
| [ui-styling](../../skills/ui-styling/SKILL.md) | Style interfaces, components, and canvas designs | Advertised |
| [ui-typography](../../skills/ui-typography/SKILL.md) | Apply interface typography guidelines | Advertised |
| [relationship-design](../../skills/relationship-design/SKILL.md) | Design AI interfaces with memory and ongoing collaboration | Advertised |
| [renaissance-architecture](../../skills/renaissance-architecture/SKILL.md) | Apply software architecture and product design principles | Advertised |
| [web-design-guidelines](../../skills/web-design-guidelines/SKILL.md) | Review web usability and accessibility | Advertised |
| [vercel-composition-patterns](../../skills/composition-patterns/SKILL.md) | Apply React component composition patterns | Advertised |
| [vercel-react-best-practices](../../skills/react-best-practices/SKILL.md) | Apply React and Next.js performance practices | Advertised |
| [vercel-react-native-skills](../../skills/react-native-skills/SKILL.md) | Apply React Native and Expo practices | Advertised |
| [vercel-react-view-transitions](../../skills/react-view-transitions/SKILL.md) | Implement React page and view transitions | Advertised |

## Research and knowledge (7)

| Skill | Purpose | Observed session status |
|---|---|---|
| [defuddle](../../skills/defuddle/SKILL.md) | Extract web page content as Markdown | Advertised |
| [notebooklm-studio](../../skills/notebooklm-studio/SKILL.md) | Manage NotebookLM sources, questions, and Studio artifacts | Advertised |
| [obsidian-bases](../../skills/obsidian-bases/SKILL.md) | Create Obsidian Bases data views | Advertised |
| [obsidian-cli](../../skills/obsidian-cli/SKILL.md) | Manage Obsidian notes and application operations | Advertised |
| [obsidian-markdown](../../skills/obsidian-markdown/SKILL.md) | Write Obsidian-flavored Markdown | Advertised |
| [paper-distiller](../../skills/paper-distiller/SKILL.md) | Explain and distill research papers with HTML visualizations | Advertised |
| [json-canvas](../../skills/json-canvas/SKILL.md) | Create JSON Canvas boards and relationship diagrams | Advertised |

## Media and visualization (5)

| Skill | Purpose | Observed session status |
|---|---|---|
| [distill-video](../../skills/distill-video/SKILL.md) | Extract and distill video, subtitles, audio, and visual evidence | Advertised |
| [manim-video](../../skills/video-use/skills/manim-video/SKILL.md) | Create mathematical and technical explanation animations | Advertised |
| [video-frames](../../skills/video-frames/SKILL.md) | Extract video frames for visual analysis | Advertised |
| [video-use](../../skills/video-use/SKILL.md) | Transcribe, edit, color grade, animate, and subtitle videos | Advertised |
| [visualize](../../skills/visualize/SKILL.md) | Create HTML visualization pages | Advertised |

## Xiaohongshu (6)

| Skill | Purpose | Observed session status |
|---|---|---|
| [xiaohongshu-skills](../../skills/xiaohongshu-skills/SKILL.md) | Entry point for the Xiaohongshu skill collection | Advertised |
| [xhs-auth](../../skills/xiaohongshu-skills/skills/xhs-auth/SKILL.md) | Manage login and authentication status | Advertised |
| [xhs-explore](../../skills/xiaohongshu-skills/skills/xhs-explore/SKILL.md) | Search posts, inspect post details, and view user profiles | Advertised |
| [xhs-interact](../../skills/xiaohongshu-skills/skills/xhs-interact/SKILL.md) | Comment, reply, like, and save posts | Advertised |
| [xhs-publish](../../skills/xiaohongshu-skills/skills/xhs-publish/SKILL.md) | Publish image posts, videos, and long-form articles | Advertised |
| [xhs-content-ops](../../skills/xiaohongshu-skills/skills/xhs-content-ops/SKILL.md) | Run combined content operations workflows | Advertised |

## Strategy and writing (4)

| Skill | Purpose | Observed session status |
|---|---|---|
| [insurgent-campaign](../../skills/insurgent-campaign/SKILL.md) | Plan marketing and communications with limited resources | Advertised |
| [negentropy-lens](../../skills/negentropy-lens/SKILL.md) | Evaluate decisions through system decay and growth | Advertised |
| [stop-slop](../../skills/stop-slop/SKILL.md) | Remove formulaic AI language from prose | Advertised |
| [writing-guidelines](../../skills/writing-guidelines/SKILL.md) | Review documentation style and clarity | Advertised |

## Export handling

- Gift-card workflow emails, cardholder names, card suffixes, card nicknames, and private note titles are replaced with configuration placeholders.
- The Paze route destination is replaced with `HOME_ADDRESS`. iOS organization, Apple Team, Bundle ID, and iCloud identifiers are also placeholders. Resolve these values from private configuration before running the workflows.
- Twelve duplicate installation entrypoints are consolidated. The older Xiaohongshu entrypoint is preserved as [legacy/xiaohongshu-skills.agents.md](legacy/xiaohongshu-skills.agents.md); its filename prevents discovery as another `SKILL.md`.
- Git metadata, virtual environments, caches, Python bytecode, session writer leases, and real `.env` files are excluded. The empty `.env.example` and required source files such as `cookies.py` are retained.
- Local installed skills were not modified. Existing repository executable permissions are preserved. Original package licenses and font notices remain with their files and apply individually.
- The installed `vercel-optimize/lib/vercel.mjs` includes Windows CLI entry resolution absent from the previous repository version. This export includes that difference.

## Installation and restoration

Clone the branch containing this export, or the default branch after the PR is merged. After merge, install an individual skill with:

```bash
npx skills add darrenfu/agent-skills --skill distill-video
```

For a manual restore, use each manifest entry's `path` to locate the package and `source_paths` to determine its original installation location. Back up any existing destination before copying the complete package. For example:

```bash
mkdir -p "$HOME/.codex/skills"
# Run only after confirming the destinations do not exist, or backing them up.
cp -R skills/distill-video "$HOME/.codex/skills/distill-video"
cp -R skills/notebooklm-studio "$HOME/.codex/skills/notebooklm-studio-Skill"
```

Restore `manim-video` with the complete `video-use` package and the five `xhs-*` skills with the complete `xiaohongshu-skills` package. Configure applications, browser extensions, ffmpeg, Python/Node dependencies, and login sessions separately according to each skill's instructions. These external workflows were not executed during export.

Verify the exported files from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, json
manifest = json.loads(Path('docs/installed-skills/manifest.json').read_text())
for entry in manifest['files']:
    path = Path(entry['path'])
    assert path.is_file() and not path.is_symlink(), path
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], path
print(f"Verified {len(manifest['files'])} exported files")
PY
```

## Existing format compatibility notes

All 50 definitions have parseable YAML with complete names and descriptions. The system's strict `quick_validate.py` reports the following seven existing metadata warnings. Their metadata is retained to preserve the installed content. All seven appeared in the session's advertised list, so these warnings are not evidence of an observed loading failure.

| Skill | Strict validation warning |
|---|---|
| `manim-video` | Unexpected key(s) in SKILL.md frontmatter: version. Allowed properties are: allowed-tools, description, license, metadata, name |
| `vercel-react-view-transitions` | Description cannot contain angle brackets (< or >) |
| `visualize` | Unexpected key(s) in SKILL.md frontmatter: argument-hint. Allowed properties are: allowed-tools, description, license, metadata, name |
| `xhs-auth` | Unexpected key(s) in SKILL.md frontmatter: version. Allowed properties are: allowed-tools, description, license, metadata, name |
| `xhs-content-ops` | Unexpected key(s) in SKILL.md frontmatter: version. Allowed properties are: allowed-tools, description, license, metadata, name |
| `xhs-interact` | Unexpected key(s) in SKILL.md frontmatter: version. Allowed properties are: allowed-tools, description, license, metadata, name |
| `xhs-publish` | Unexpected key(s) in SKILL.md frontmatter: version. Allowed properties are: allowed-tools, description, license, metadata, name |

Validation covers export integrity, structure, private configuration replacement, and affected scripts. It does not establish that every skill's login, purchase, deployment, device operation, or external service workflow has been tested.
