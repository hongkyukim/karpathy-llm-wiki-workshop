#!/usr/bin/env python3
import argparse
import re
import shutil
import subprocess
from collections import defaultdict
from pathlib import Path

LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def label(stem: str) -> str:
    return stem.replace("-", " ")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default="vault")
    ap.add_argument("--out", default="docs/graph")
    args = ap.parse_args()
    vault = Path(args.vault)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    pages = [p for folder in ["entities", "concepts", "comparisons", "queries"] for p in (vault / folder).glob("*.md")]
    stems = {p.stem for p in pages}
    edges = set()
    inbound = defaultdict(int)
    for p in pages:
        text = p.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            target_stem = target.strip().lower().replace(" ", "-")
            edges.add((p.stem, target_stem))
            inbound[target_stem] += 1
    dot = ["digraph LLMWiki {", "  rankdir=LR;", "  node [shape=box, style=rounded];"]
    for stem in sorted(stems | {t for _, t in edges}):
        color = "lightgray" if stem not in stems else "white"
        dot.append(f'  "{stem}" [label="{label(stem)}", fillcolor="{color}", style="rounded,filled"];')
    for a, b in sorted(edges):
        dot.append(f'  "{a}" -> "{b}";')
    dot.append("}")
    dot_path = out / "graph.dot"
    dot_path.write_text("\n".join(dot) + "\n", encoding="utf-8")
    md = ["# LLM Wiki Graph", "", f"Pages: {len(stems)}", f"Edges: {len(edges)}", "", "## Hubs", ""]
    for stem, count in sorted(inbound.items(), key=lambda kv: (-kv[1], kv[0]))[:20]:
        md.append(f"- [[{stem}]] — {count} inbound links")
    md += ["", "## Edges", ""]
    for a, b in sorted(edges):
        md.append(f"- [[{a}]] → [[{b}]]")
    (out / "graph.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    dot_bin = shutil.which("dot")
    if dot_bin:
        subprocess.run([dot_bin, "-Tsvg", str(dot_path), "-o", str(out / "graph.svg")], check=True)
        print(f"Wrote {dot_path}, {out / 'graph.md'}, and {out / 'graph.svg'}")
    else:
        print(f"Wrote {dot_path} and {out / 'graph.md'}; install Graphviz for SVG export")

if __name__ == "__main__":
    main()
