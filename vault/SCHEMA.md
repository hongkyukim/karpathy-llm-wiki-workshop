# Wiki Schema

## Domain
LLM systems, model training, local inference, LLM application frameworks, and GitHub repositories used as source material for learning and technical reconnaissance.

## Conventions
- File names: lowercase, hyphens, no spaces.
- Every curated wiki page starts with YAML frontmatter.
- Use Obsidian `[[wikilinks]]` between pages.
- Each curated page should have at least two outbound links when possible.
- Raw source files under `raw/` are immutable after capture.
- Every curated page must appear in `index.md`.
- Every action must be appended to `log.md`.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [repo, training]
sources: [raw/github/example.json]
confidence: high | medium | low
---
```

## Raw source frontmatter
```yaml
---
source_url: https://github.com/owner/repo
ingested: YYYY-MM-DD
sha256: <hex digest of raw body>
---
```

## Tag Taxonomy
- repo: GitHub repository entity pages
- person: people and maintainers
- organization: companies, labs, communities
- training: model training code and techniques
- inference: serving and local runtime topics
- systems: performance, kernels, CUDA, C/C++, systems engineering
- application-framework: agent, chain, orchestration, app framework topics
- rag: retrieval-augmented generation and alternatives
- obsidian: vault, wikilink, note-taking, graph-view topics
- provenance: source capture, hashing, citations, drift detection
- graph: graph analysis, wikilinks, relationships
- comparison: side-by-side analysis

## Page Thresholds
- Create a repo entity page for every repo listed in `data/repos.json`.
- Create concept pages for central ideas found across multiple repos or central to one source.
- Do not create pages for passing mentions.
- Split pages over ~200 lines.

## Update Policy
When sources conflict, keep both claims with dated provenance, mark confidence, and flag for review in `log.md`.
