# Vercel Agent Skills - Codex Port

Codex-compatible skill port of `vercel-labs/agent-skills`.

## Skills

- `vercel-composition-patterns`
- `deploy-to-vercel`
- `vercel-react-best-practices`
- `vercel-react-native-skills`
- `vercel-react-view-transitions`
- `vercel-cli-with-tokens`
- `vercel-optimize`
- `web-design-guidelines`
- `writing-guidelines`

## Install Locally

```bash
mkdir -p "$HOME/.codex/skills"
cp -R skills/* "$HOME/.codex/skills/"
```

Restart Codex after installation.

## Validation

```bash
for skill in skills/*; do
  python3 "$HOME/.codex/skills/.system/skill-creator/scripts/quick_validate.py" "$skill"
done
```

## Porting Notes

- Frontmatter is normalized to Codex's accepted fields.
- `agents/openai.yaml` is added for Codex UI metadata.
- Bundled scripts, references, data, and assets are preserved where useful.
- Broad creative helper skills may set `allow_implicit_invocation: false`; invoke them explicitly with `$skill-name`.
