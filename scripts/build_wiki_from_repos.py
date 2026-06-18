#!/usr/bin/env python3
import argparse
import json
import re
from datetime import date
from pathlib import Path

CONCEPT_RULES = {
    "training": ["train", "training", "gpt", "transformer", "dataset"],
    "local-llm-inference": ["inference", "quantization", "local", "runtime", "serve"],
    "llm-application-frameworks": ["agent", "chain", "rag", "retrieval", "tool"],
    "systems-performance": ["cuda", "c++", "kernel", "performance", "gpu"],
    "obsidian-llm-wiki": ["wiki", "obsidian", "graph", "markdown", "wikilink"],
}

CONCEPT_TITLES = {
    "training": "Training",
    "local-llm-inference": "Local LLM Inference",
    "llm-application-frameworks": "LLM Application Frameworks",
    "systems-performance": "Systems Performance",
    "obsidian-llm-wiki": "Obsidian LLM Wiki",
}


def strip_frontmatter(text: str) -> str:
    if text.startswith("---\n"):
        parts = text.split("---\n", 2)
        if len(parts) == 3:
            return parts[2]
    return text


def repo_slug(raw_json: Path) -> str:
    return raw_json.stem


def title_from_slug(slug: str) -> str:
    return slug.split("--", 1)[-1]


def frontmatter(title, typ, tags, sources, confidence="medium"):
    today = date.today().isoformat()
    src = ", ".join(sources)
    tag_s = ", ".join(tags)
    return f"---\ntitle: {title}\ncreated: {today}\nupdated: {today}\ntype: {typ}\ntags: [{tag_s}]\nsources: [{src}]\nconfidence: {confidence}\n---\n\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default="vault")
    args = ap.parse_args()
    vault = Path(args.vault)
    raw_dir = vault / "raw" / "github"
    entity_dir = vault / "entities"
    concept_dir = vault / "concepts"
    comp_dir = vault / "comparisons"
    for d in [entity_dir, concept_dir, comp_dir]:
        d.mkdir(parents=True, exist_ok=True)
    repos = []
    concept_hits = {key: [] for key in CONCEPT_RULES}
    for raw_json in sorted(raw_dir.glob("*.json")):
        data = json.loads(strip_frontmatter(raw_json.read_text(encoding="utf-8")))
        slug = repo_slug(raw_json)
        repo_name = data["repo"]
        text = " ".join(str(data.get(k, "")) for k in ["description", "focus", "language", "topics", "readme_excerpt"]).lower()
        hits = []
        for concept, words in CONCEPT_RULES.items():
            if any(w in text for w in words):
                hits.append(concept)
                concept_hits[concept].append(slug)
        if not hits:
            hits = ["llm-application-frameworks"]
            concept_hits[hits[0]].append(slug)
        links = " ".join(f"[[{h}]]" for h in hits[:3])
        md = frontmatter(repo_name, "entity", ["repo"], [f"raw/github/{raw_json.name}"]) + f"# {repo_name}\n\n"
        md += f"GitHub repository: {data.get('url')}\n\n"
        md += f"{data.get('description') or 'No description captured.'}\n\n"
        md += f"Workshop focus: {data.get('focus') or 'Source repository for the LLM Wiki workshop.'}\n\n"
        md += "## Snapshot\n\n"
        md += f"- Owner: {data.get('owner')}\n- Primary language: {data.get('language')}\n- Stars at capture: {data.get('stars')}\n- Topics: {', '.join(data.get('topics') or []) or 'none captured'}\n- License: {data.get('license') or 'unknown'}\n\n"
        md += "## Related concepts\n\n" + links + "\n\n"
        md += "## Notes for curation\n\n- Verify whether generated concept links are central or incidental.\n- Add backlinks from related concept pages after human review.\n"
        (entity_dir / f"{slug}.md").write_text(md, encoding="utf-8")
        repos.append((slug, repo_name, data))
    for concept, slugs in concept_hits.items():
        if not slugs:
            continue
        title = CONCEPT_TITLES[concept]
        links = " ".join(f"[[{s}]]" for s in sorted(set(slugs)))
        md = frontmatter(title, "concept", [concept if concept in ["training", "graph"] else "systems" if concept == "systems-performance" else "inference" if concept == "local-llm-inference" else "application-framework" if concept == "llm-application-frameworks" else "obsidian"], ["raw/github/*.json"]) + f"# {title}\n\n"
        md += f"This concept page was generated from GitHub repository captures that mention or demonstrate {title.lower()}.\n\n"
        md += "## Related repositories\n\n" + links + "\n\n"
        md += "## Open questions\n\n- Which claims should be promoted from generated notes to high-confidence statements?\n- Which repositories provide the clearest runnable example for this concept?\n"
        (concept_dir / f"{concept}.md").write_text(md, encoding="utf-8")
    rows = []
    for slug, name, data in repos:
        rows.append(f"| [[{slug}]] | {data.get('language') or ''} | {data.get('stars') or ''} | {data.get('focus') or ''} |")
    comp = frontmatter("GitHub Repo Landscape", "comparison", ["comparison", "repo"], ["raw/github/*.json"]) + "# GitHub Repo Landscape\n\n"
    comp += "| Repository | Language | Stars at capture | Workshop focus |\n|---|---:|---:|---|\n" + "\n".join(rows) + "\n\n"
    comp += "Related concepts: [[training]] [[local-llm-inference]] [[llm-application-frameworks]] [[systems-performance]]\n"
    (comp_dir / "github-repo-landscape.md").write_text(comp, encoding="utf-8")
    pages = []
    for folder in ["entities", "concepts", "comparisons", "queries"]:
        for p in sorted((vault / folder).glob("*.md")):
            if p.name == ".gitkeep":
                continue
            text = p.read_text(encoding="utf-8")
            title = re.search(r"^title:\s*(.+)$", text, re.M)
            summary = "generated workshop page"
            pages.append((folder, p.stem, title.group(1) if title else p.stem, summary))
    today = date.today().isoformat()
    sections = {"entities": [], "concepts": [], "comparisons": [], "queries": []}
    for folder, stem, title, summary in pages:
        sections[folder].append(f"- [[{stem}]] — {summary}")
    index = f"# Wiki Index\n\n> Content catalog. Every curated wiki page listed under its type with a one-line summary.\n> Last updated: {today} | Total pages: {len(pages)}\n\n"
    for folder, heading in [("entities", "Entities"), ("concepts", "Concepts"), ("comparisons", "Comparisons"), ("queries", "Queries")]:
        index += f"## {heading}\n\n" + "\n".join(sections[folder]) + "\n\n"
    (vault / "index.md").write_text(index, encoding="utf-8")
    with (vault / "log.md").open("a", encoding="utf-8") as f:
        f.write(f"\n## [{today}] ingest | GitHub repository batch\n- Created/updated {len(pages)} curated pages from {len(repos)} GitHub repo captures.\n")
    print(f"Built {len(pages)} wiki pages from {len(repos)} repositories")

if __name__ == "__main__":
    main()
