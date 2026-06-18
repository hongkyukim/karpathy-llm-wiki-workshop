# Lab 4 — Graphify the wiki

## Goal

Export wikilinks and source relationships into a graph that can be inspected outside Obsidian.

## Steps

```bash
python scripts/graphify_wiki.py --vault vault --out docs/graph
```

Outputs:

- `docs/graph/graph.dot`
- `docs/graph/graph.md`
- `docs/graph/graph.svg` if Graphviz `dot` is installed

## Analysis prompts

1. Which concepts are hubs?
2. Which repo pages are isolated?
3. What backlinks should be added?
4. Which missing comparison page would make the graph more useful?

## Maintenance loop

```bash
python scripts/validate_workshop.py --vault vault --graph docs/graph/graph.dot
```

Fix broken links before adding more sources.
