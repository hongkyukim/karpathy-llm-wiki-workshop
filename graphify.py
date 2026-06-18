#!/usr/bin/env python3
"""
graphify.py — Obsidian Wiki Knowledge Graph Visualiser
======================================================
Parses [[wiki links]] from Markdown notes in an Obsidian vault and renders
the resulting knowledge graph as:
  - graph.png   (static PNG via matplotlib / networkx)
  - graph.json  (node + edge list for downstream processing)

Usage
-----
    python graphify.py
    python graphify.py --notes-dir notes --output graph.png --json graph.json
    python graphify.py --no-show          # skip interactive window (CI-friendly)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

WIKI_LINK_RE = re.compile(r"\[\[([^\[\]|#\n]+?)(?:\|[^\[\]\n]*)?\]\]")


def _stem(path: Path) -> str:
    """Return the note's display name (filename without .md extension)."""
    return path.stem


def parse_links(md_text: str) -> list[str]:
    """Return a list of link targets found in *md_text* (raw [[…]] targets)."""
    return [m.group(1).strip() for m in WIKI_LINK_RE.finditer(md_text)]


def build_graph(notes_dir: Path) -> tuple[set[str], list[tuple[str, str]]]:
    """
    Walk *notes_dir*, parse every .md file, and return:
        nodes — set of note names
        edges — list of (source, target) directed edges
    Only edges whose target exists as a note are included.
    """
    note_files = list(notes_dir.rglob("*.md"))
    nodes: set[str] = {_stem(f) for f in note_files}
    edges: list[tuple[str, str]] = []

    seen: set[tuple[str, str]] = set()
    for note_file in sorted(note_files):
        source = _stem(note_file)
        text = note_file.read_text(encoding="utf-8", errors="replace")
        for target in parse_links(text):
            # Ignore links to non-existent notes (e.g. external references)
            # and deduplicate repeated links within the same file
            if target in nodes and target != source and (source, target) not in seen:
                seen.add((source, target))
                edges.append((source, target))

    return nodes, edges


# ---------------------------------------------------------------------------
# JSON export
# ---------------------------------------------------------------------------

def export_json(nodes: set[str], edges: list[tuple[str, str]], output_path: Path) -> None:
    data = {
        "nodes": sorted(nodes),
        "edges": [{"source": s, "target": t} for s, t in edges],
    }
    output_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"[graphify] JSON written → {output_path}")


# ---------------------------------------------------------------------------
# PNG export (requires networkx + matplotlib)
# ---------------------------------------------------------------------------

def export_png(
    nodes: set[str],
    edges: list[tuple[str, str]],
    output_path: Path,
    show: bool = True,
) -> None:
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError as exc:
        print(
            f"[graphify] WARNING: Cannot generate PNG — {exc}\n"
            "           Install dependencies with:  pip install -r requirements.txt",
            file=sys.stderr,
        )
        return

    G = nx.DiGraph()
    G.add_nodes_from(sorted(nodes))
    G.add_edges_from(edges)

    # Compute node degree for sizing
    degree = dict(G.degree())
    node_sizes = [300 + degree.get(n, 0) * 120 for n in G.nodes()]

    # Use a spring layout seeded for reproducibility
    pos = nx.spring_layout(G, seed=42, k=2.5 / max(len(nodes) ** 0.5, 1))

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_title(
        "Karpathy LLM Wiki — Knowledge Graph",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.axis("off")

    # Draw edges
    nx.draw_networkx_edges(
        G, pos,
        ax=ax,
        edge_color="#aaaaaa",
        arrows=True,
        arrowsize=12,
        width=1.2,
        alpha=0.6,
        connectionstyle="arc3,rad=0.05",
    )

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        ax=ax,
        node_size=node_sizes,
        node_color="#4C72B0",
        alpha=0.85,
    )

    # Draw labels
    nx.draw_networkx_labels(
        G, pos,
        ax=ax,
        font_size=8,
        font_color="white",
        font_weight="bold",
    )

    # Stats legend
    stats = mpatches.Patch(
        color="#4C72B0",
        label=f"{len(nodes)} notes · {len(edges)} links",
    )
    ax.legend(handles=[stats], loc="lower right", fontsize=10)

    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"[graphify] PNG written  → {output_path}")

    if show:
        plt.show()
    plt.close(fig)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visualise an Obsidian Markdown vault as a knowledge graph.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--notes-dir",
        default="notes",
        metavar="DIR",
        help="Path to the Obsidian notes directory",
    )
    parser.add_argument(
        "--output",
        default="graph.png",
        metavar="FILE",
        help="Output path for the PNG graph image",
    )
    parser.add_argument(
        "--json",
        default="graph.json",
        metavar="FILE",
        help="Output path for the JSON node/edge list",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open an interactive matplotlib window",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    notes_dir = Path(args.notes_dir)
    if not notes_dir.is_dir():
        print(
            f"[graphify] ERROR: notes directory '{notes_dir}' not found.",
            file=sys.stderr,
        )
        return 1

    print(f"[graphify] Scanning notes in '{notes_dir}' …")
    nodes, edges = build_graph(notes_dir)

    if not nodes:
        print("[graphify] No Markdown files found.", file=sys.stderr)
        return 1

    print(f"[graphify] Found {len(nodes)} notes and {len(edges)} links.")

    export_json(nodes, edges, Path(args.json))
    export_png(nodes, edges, Path(args.output), show=not args.no_show)

    return 0


if __name__ == "__main__":
    sys.exit(main())
