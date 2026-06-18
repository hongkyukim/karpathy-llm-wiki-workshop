# Lab 1 — Initialize an Obsidian LLM Wiki vault

## Goal

Create the three-layer wiki structure: raw sources, curated wiki pages, and schema/navigation files.

## Steps

```bash
python scripts/init_vault.py --vault vault
```

Inspect:

- `vault/SCHEMA.md`
- `vault/index.md`
- `vault/log.md`
- `vault/raw/`
- `vault/entities/`, `vault/concepts/`, `vault/comparisons/`, `vault/queries/`

## Discussion

Answer as a group:

1. What should be immutable?
2. What should the agent be allowed to edit?
3. Which tags belong in the schema before first ingestion?
4. How is this different from uploading files into a RAG chat?

## Checkpoint

```bash
python scripts/validate_workshop.py --vault vault
```
