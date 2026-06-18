# Karpathy LLM Wiki Workshop: Obsidian + GitHub Repo Graphs

A hands-on workshop for building a Karpathy-style LLM Wiki: a persistent, compounding knowledge base where an agent incrementally turns source material into interlinked Markdown pages instead of re-discovering chunks on every query.

This workshop uses GitHub repositories as the source corpus, Obsidian as the human-readable vault, and graph exports to make repository/concept relationships visible.

## What you will build

By the end, attendees will have:

- an Obsidian-compatible wiki vault under `vault/`
- raw immutable GitHub repo source captures under `vault/raw/github/`
- curated concept/entity/comparison pages with `[[wikilinks]]`
- a graph export in DOT, Markdown, and SVG/PNG when Graphviz is available
- prompts for agent-assisted ingestion, synthesis, linting, and maintenance
- validation scripts that catch broken links, missing frontmatter, and graph issues

## Why this is different from RAG

RAG retrieves raw chunks at question time. A Karpathy-style LLM Wiki compiles knowledge over time:

1. capture raw sources immutably
2. extract entities and concepts into durable pages
3. cross-link pages so synthesis compounds
4. keep provenance and update logs
5. answer questions from the maintained wiki, not from a fresh retrieval pass

## Local-first quickstart

No cloud credentials are required for the default path.

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt

# Create an Obsidian-compatible vault skeleton.
python scripts/init_vault.py --vault vault

# Fetch public GitHub repo metadata/README files using unauthenticated GitHub API.
python scripts/fetch_github_repos.py --repos data/repos.json --vault vault

# Build first-pass wiki pages from captured repo sources.
python scripts/build_wiki_from_repos.py --vault vault

# Export the wikilink/repo graph.
python scripts/graphify_wiki.py --vault vault --out docs/graph

# Validate workshop artifacts.
python scripts/validate_workshop.py --vault vault --graph docs/graph/graph.dot
```

Or run the whole local path:

```bash
make demo
```

Open `vault/` in Obsidian and use Graph View. If Graphviz `dot` is installed, `docs/graph/graph.svg` is also generated.

## Workshop formats

### 60-minute version

- 0-10 min: Karpathy LLM Wiki concept and Obsidian vault shape
- 10-25 min: Lab 1 — initialize the vault and inspect schema/index/log
- 25-40 min: Lab 2 — fetch GitHub repos and build first-pass pages
- 40-55 min: Lab 3 — graphify links and use the graph to identify missing relationships
- 55-60 min: wrap-up and next ingestion targets

### Half-day version

- Module 1: LLM Wiki mental model vs RAG
- Module 2: Obsidian vault conventions and provenance
- Module 3: GitHub repos as source material
- Module 4: Agent-assisted page creation and cross-linking
- Module 5: Graph analysis and quality gates
- Module 6: maintenance workflows and team publishing

## Repository structure

```text
data/repos.json                 Public GitHub repos used in the default lab
labs/                           Step-by-step attendee labs
prompts/                        Agent prompts for ingestion/synthesis/linting
scripts/                        Local workshop automation
vault/.gitkeep                  Generated Obsidian vault lives here
requirements.txt                Optional Python dependencies; default scripts use stdlib
```

## Optional GitHub publishing

After completing the local lab, create a new GitHub repository and push this workshop:

```bash
git remote add origin git@github.com:<owner>/karpathy-llm-wiki-workshop.git
git branch -M main
git push -u origin main
```

Do not commit private vault notes, tokens, or credentials. `.gitignore` excludes generated raw captures and local environments by default.

## Optional Obsidian setup

- Open `vault/` as an Obsidian vault.
- Keep Wikilinks enabled.
- Set attachment folder to `raw/assets/`.
- Optional community plugins: Dataview, Excalidraw, Obsidian Git.

## Source inspiration

- Andrej Karpathy, “LLM Wiki” gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- GitHub REST API docs: https://docs.github.com/en/rest
- Obsidian help: https://help.obsidian.md/
