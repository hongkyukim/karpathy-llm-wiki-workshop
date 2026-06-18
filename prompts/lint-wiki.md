# Prompt — Lint the LLM Wiki

Audit the wiki for:

- broken `[[wikilinks]]`
- orphan pages with no inbound links
- pages missing YAML frontmatter
- pages not listed in `index.md`
- tags not listed in `SCHEMA.md`
- raw source hash drift
- pages over 200 lines
- low-confidence or contested claims

Report findings grouped by severity and append a `lint` entry to `log.md`.
