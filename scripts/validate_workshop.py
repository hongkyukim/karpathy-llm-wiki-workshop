#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
REQ_FM = ["title:", "created:", "updated:", "type:", "tags:", "sources:"]


def has_frontmatter(text: str) -> bool:
    return text.startswith("---\n") and "\n---\n" in text[4:]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default="vault")
    ap.add_argument("--graph", default=None)
    args = ap.parse_args()
    vault = Path(args.vault)
    issues = []
    for required in ["SCHEMA.md", "index.md", "log.md", "raw", "entities", "concepts", "comparisons", "queries"]:
        if not (vault / required).exists():
            issues.append(f"missing {vault / required}")
    pages = [p for folder in ["entities", "concepts", "comparisons", "queries"] for p in (vault / folder).glob("*.md")]
    stems = {p.stem for p in pages}
    index = (vault / "index.md").read_text(encoding="utf-8") if (vault / "index.md").exists() else ""
    for p in pages:
        text = p.read_text(encoding="utf-8")
        if not has_frontmatter(text):
            issues.append(f"missing frontmatter: {p}")
        else:
            fm = text.split("---\n", 2)[1]
            for key in REQ_FM:
                if key not in fm:
                    issues.append(f"frontmatter missing {key} in {p}")
        if f"[[{p.stem}]]" not in index:
            issues.append(f"page missing from index: {p}")
        for link in LINK_RE.findall(text):
            stem = link.strip().lower().replace(" ", "-")
            if stem not in stems:
                issues.append(f"broken wikilink in {p}: [[{link}]]")
    if args.graph and not Path(args.graph).exists():
        issues.append(f"missing graph file: {args.graph}")
    if issues:
        print("Validation failed:")
        for i in issues:
            print(f"- {i}")
        sys.exit(1)
    print(f"Validation passed: {len(pages)} pages checked")

if __name__ == "__main__":
    main()
