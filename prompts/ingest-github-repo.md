# Prompt — Ingest a GitHub repo into the LLM Wiki

You are maintaining a Karpathy-style LLM Wiki in an Obsidian vault.

Before editing:
1. Read `SCHEMA.md`.
2. Read `index.md`.
3. Read recent `log.md` entries.
4. Read the raw GitHub source capture under `raw/github/`.

Task:
- Create or update one entity page for the repository.
- Create or update concept pages for central technical ideas only.
- Add at least two outbound `[[wikilinks]]` per generated page.
- Add provenance references to the raw source file.
- Update `index.md` alphabetically.
- Append a log entry.
- Do not modify `raw/` files.

Quality rules:
- Use only tags already listed in `SCHEMA.md`; update schema first if a new tag is necessary.
- Mark low-confidence claims as `confidence: medium` or `confidence: low` in frontmatter.
- Do not create pages for passing mentions.
