# Lab 2 — Capture GitHub repositories as raw sources

## Goal

Use public GitHub repositories as source material for an LLM Wiki.

## Steps

```bash
python scripts/fetch_github_repos.py --repos data/repos.json --vault vault
```

The script captures:

- repository metadata
- README markdown
- language/topic/license/star summaries
- a source hash for drift detection

Raw files are written under `vault/raw/github/`. Treat them as immutable after capture.

## Optional authenticated mode

Unauthenticated GitHub API calls are rate limited. For larger workshops:

```bash
GITHUB_TOKEN=<token> python scripts/fetch_github_repos.py --repos data/repos.json --vault vault
```

## Checkpoint

```bash
python - <<'PY'
from pathlib import Path
for p in sorted(Path('vault/raw/github').glob('*')):
    print(p)
PY
```
