# MLP — Multi-Layer Perceptron

> **Tags:** #architecture #foundation
> **Related:** [[Neural-Network]], [[Embedding]], [[Backpropagation]], [[Training]], [[Loss-Function]], [[Bigram-Model]]

---

## What Is an MLP?

A **Multi-Layer Perceptron (MLP)** is a [[Neural-Network]] with one or more **hidden layers** between input and output.  Compared to the [[Bigram-Model]], an MLP:
- Takes a *window* of previous tokens as context (not just 1).
- Learns compact [[Embedding|embeddings]] for each token.
- Can capture richer statistical patterns.

---

## Bengio et al. (2003) — Karpathy makemore Part 2

Karpathy implements the classic 2003 paper by Bengio et al.:

```
tokens  →  [[Embedding]] lookup  →  concat  →  Linear  →  tanh  →  Linear  →  [[Softmax]]
```

```python
# Embedding lookup
emb = C[X]                          # (B, context_len, emb_dim)
x   = emb.view(B, -1)               # flatten: (B, context_len * emb_dim)

# Hidden layer
h   = torch.tanh(x @ W1 + b1)      # (B, hidden_size)

# Output logits
logits = h @ W2 + b2                # (B, vocab_size)
```

---

## Architecture Details

| Component | Typical Values |
|-----------|---------------|
| Context length | 3–8 tokens |
| Embedding dim | 10–64 |
| Hidden size | 100–512 |
| Output size | vocab size (e.g. 27 for characters) |

---

## Activations

- **tanh** — squashes output to (−1, 1), historically common
- **ReLU** — `max(0, x)`, most popular for large networks
- **GELU** — smooth ReLU variant used in [[GPT]]

---

## MLP Block Inside a Transformer

In the [[Transformer]], each layer contains a small MLP (often called the **FFN — Feed-Forward Network**):

```
x  →  LayerNorm  →  Linear(d_model → 4*d_model)  →  GELU  →  Linear(4*d_model → d_model)  →  + x
```

This is where the model stores "factual" information after the [[Attention]] mechanism selects relevant context.

---

## Karpathy Resources

- makemore Part 2 — [YouTube](https://youtu.be/TCH_1BHY58I)
