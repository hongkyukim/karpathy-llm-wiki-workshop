# Karpathy LLM Wiki Workshop

A structured knowledge base for learning Large Language Models (LLMs) through Andrej Karpathy's lectures and resources, organised as an **Obsidian vault** and visualised with the included **Graphify** tool.

---

## 📚 What Is This?

This repo contains:

| Path | Purpose |
|------|---------|
| `notes/` | Obsidian-compatible Markdown notes with `[[wiki links]]` |
| `graphify.py` | Python script that parses the notes and renders an interactive knowledge graph |
| `requirements.txt` | Python dependencies for `graphify.py` |

---

## 🗂️ Notes (Obsidian Vault)

Open the `notes/` directory as an **Obsidian vault** (*File → Open Vault → select the `notes` folder*).  
Every concept note links to related concepts via `[[wiki links]]`, so Obsidian's *Graph View* automatically shows the knowledge network.

Start here: **[notes/00-Index.md](notes/00-Index.md)**

### Core Concepts Covered

- [[LLM]] — Large Language Models overview
- [[Neural-Network]] — foundations
- [[Bigram-Model]] — simplest language model (makemore series)
- [[MLP]] — Multi-Layer Perceptron
- [[Transformer]] — the dominant architecture
- [[Attention]] — self-attention mechanism
- [[Embedding]] — token & positional embeddings
- [[Softmax]] — probability over vocabulary
- [[Loss-Function]] — cross-entropy & perplexity
- [[Tokenization]] — BPE & subword tokenisation
- [[GPT]] — GPT architecture end-to-end
- [[Training]] — gradient descent & optimisers
- [[Backpropagation]] — computing gradients

---

## 🔭 Graphify Tool

`graphify.py` reads every `.md` file in `notes/`, extracts `[[wiki links]]`, builds a directed graph, and produces:

- `graph.png` — static PNG visualisation
- `graph.json` — JSON node/edge list for further use

### Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate the graph (reads notes/ by default)
python graphify.py

# Custom notes directory or output path
python graphify.py --notes-dir notes --output graph.png
```

### Options

```
usage: graphify.py [-h] [--notes-dir NOTES_DIR] [--output OUTPUT] [--json JSON] [--no-show]

options:
  --notes-dir   Path to the Obsidian notes directory (default: notes)
  --output      Path for the PNG output           (default: graph.png)
  --json        Path for the JSON output          (default: graph.json)
  --no-show     Do not open an interactive window (useful for CI/scripts)
```

---

## 🔗 Key Karpathy Resources

| Resource | Link |
|----------|------|
| makemore series (character-level LMs) | https://github.com/karpathy/makemore |
| Let's build GPT (from scratch) | https://youtu.be/kCc8FmEb1nY |
| Let's build the GPT Tokenizer | https://youtu.be/zduSFxRajkE |
| nanoGPT repository | https://github.com/karpathy/nanoGPT |
| llm.c repository | https://github.com/karpathy/llm.c |
