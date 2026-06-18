# Transformer

> **Tags:** #architecture
> **Related:** [[Attention]], [[MLP]], [[Embedding]], [[GPT]], [[LLM]], [[Training]]

---

## What Is the Transformer?

The **Transformer** (Vaswani et al., 2017 — *"Attention Is All You Need"*) is the dominant neural architecture for language modelling.  It replaces recurrence (RNNs/LSTMs) with **self-attention**, enabling:

- Fully parallel training across all sequence positions.
- Direct modelling of long-range dependencies.
- Efficient scaling to billions of parameters.

---

## Architecture Overview

```
Input tokens
     │
  [[Tokenization]]  →  token IDs
     │
  [[Embedding]] (token + positional)
     │
  ┌──────────────────────────────┐
  │  Transformer Block × N       │
  │                              │
  │   LayerNorm                  │
  │       │                      │
  │  [[Attention|CausalSelfAttention]]  │
  │       │  + residual           │
  │   LayerNorm                  │
  │       │                      │
  │   [[MLP|Feed-Forward (MLP)]] │
  │       │  + residual           │
  └──────────────────────────────┘
     │
  LayerNorm
     │
  Linear (lm_head)  →  logits (vocab_size)
     │
  [[Softmax]]  →  probabilities
```

---

## Key Design Choices

| Choice | Benefit |
|--------|---------|
| **Residual connections** | Allow gradients to flow → enables very deep networks |
| **Layer Normalisation** | Stabilises training |
| **Multi-Head [[Attention]]** | Different heads capture different patterns |
| **[[MLP]] after attention** | Stores factual knowledge; expands + contracts dimension |

---

## GPT vs. Original Transformer

| Feature | Transformer (2017) | GPT-2/3 |
|---------|-------------------|---------|
| Encoder | ✅ | ❌ (decoder-only) |
| Decoder | ✅ | ✅ |
| Cross-attention | ✅ | ❌ |
| Causal masking | ✅ (decoder) | ✅ (all layers) |

GPT is a **decoder-only** transformer — it only predicts the next token, never attends to future positions.

---

## Scaling Laws

Research (Kaplan et al., 2020; Hoffmann et al., 2022) shows that loss decreases predictably as:
- Model parameters increase
- Dataset tokens increase
- Compute budget increases

This motivates training larger models on more data (→ [[LLM]]).

---

## Karpathy Resources

- Let's build GPT — [YouTube](https://youtu.be/kCc8FmEb1nY) — build the full Transformer
- [nanoGPT model.py](https://github.com/karpathy/nanoGPT/blob/master/model.py)
