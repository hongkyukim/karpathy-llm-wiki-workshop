# Lab 3 — Build first-pass wiki pages

## Goal

Turn repo source captures into Obsidian pages that accumulate knowledge.

## Steps

```bash
python scripts/build_wiki_from_repos.py --vault vault
```

Inspect generated pages:

- `vault/entities/*.md`
- `vault/concepts/*.md`
- `vault/comparisons/github-repo-landscape.md`
- `vault/index.md`
- `vault/log.md`

## Human curation exercise

Pick one generated concept page and improve it manually or with an agent:

- add one missing `[[wikilink]]`
- clarify a weak claim
- add a question under “Open questions”
- verify tags against `SCHEMA.md`

Use `prompts/ingest-github-repo.md` for an agent-assisted variant.

## Checkpoint

```bash
python scripts/validate_workshop.py --vault vault
```
