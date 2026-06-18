# Embedding

> **Tags:** #representation #foundation
> **Related:** [[Tokenization]], [[MLP]], [[Transformer]], [[Attention]], [[Neural-Network]]

---

## What Is an Embedding?

An **embedding** maps a discrete token ID to a dense, continuous vector of fixed dimensionality.  Instead of a sparse one-hot vector, every token is represented as a point in a learned **embedding space**.

```
token_id (integer)  →  Embedding table lookup  →  dense vector (float)
                              (vocab_size × d_model)
```

---

## Token Embeddings

A learnable matrix **C** (or **wte** in GPT code) of shape `(vocab_size, d_model)`:

```python
C = nn.Embedding(vocab_size, d_model)
x = C(token_ids)   # shape: (B, T, d_model)
```

Semantically similar tokens end up with similar vectors after training.

---

## Positional Embeddings

[[Attention]] is order-agnostic — it treats the input as a *set* of tokens.  To inject sequence order we add a **positional embedding**:

```python
wpe = nn.Embedding(context_len, d_model)
pos  = torch.arange(T)            # [0, 1, 2, ..., T-1]
x    = token_emb + wpe(pos)       # add position info
```

Karpathy uses **learned** positional embeddings in nanoGPT.  The original *Attention Is All You Need* paper used sinusoidal functions.

---

## Embedding Dimension

| Model | d_model |
|-------|---------|
| GPT-2 small | 768 |
| GPT-2 medium | 1024 |
| GPT-2 large | 1280 |
| GPT-2 XL | 1600 |
| GPT-3 | 12 288 |

---

## Geometry of Embedding Space

Famous example from word2vec:

```
king − man + woman ≈ queen
```

LLM embeddings encode much richer structure — syntax, semantics, and world knowledge.

---

## Connection to Other Concepts

- [[Tokenization]] determines the vocab and thus the size of the embedding table.
- [[Attention]] operates on the embedded vectors.
- [[MLP]] in the Transformer further transforms the embeddings.
- The final layer projects embeddings back to logits (the **unembedding** or **lm_head**).

---

## Karpathy Resources

- makemore Part 2 — embedding lookup tables
- Let's build GPT — `wte` and `wpe` in nanoGPT
