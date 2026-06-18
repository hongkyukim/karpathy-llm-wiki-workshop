# Softmax

> **Tags:** #operation #foundation
> **Related:** [[Loss-Function]], [[Attention]], [[Neural-Network]], [[GPT]]

---

## What Is Softmax?

**Softmax** converts a vector of arbitrary real numbers (logits) into a valid **probability distribution** — non-negative values that sum to 1.

```
softmax(z)_i  =  exp(z_i) / Σ_j exp(z_j)
```

---

## Why `exp`?

- Makes all values positive.
- Amplifies the largest value (creates sharper distributions).
- Temperature controls how sharp or flat the distribution is.

---

## Temperature Scaling

```
softmax(z / T)_i  =  exp(z_i / T) / Σ_j exp(z_j / T)
```

| Temperature T | Effect |
|--------------|--------|
| T → 0 | argmax (always picks the highest logit) |
| T = 1 | standard softmax |
| T > 1 | flatter, more random distribution |

Temperature is a key inference hyperparameter for sampling diversity in [[LLM]] text generation.

---

## Use in Language Models

The final layer of a language model produces **logits** of shape `(vocab_size,)`.  Softmax turns these into word probabilities:

```python
logits = model(x)               # (B, T, vocab_size)
probs  = F.softmax(logits, dim=-1)
```

---

## Use in Attention

[[Attention]] also uses softmax to normalise the **attention scores** between tokens:

```
attention_weights = softmax(Q @ K.T / sqrt(d_k))
```

The `sqrt(d_k)` scaling prevents extreme values that cause gradients to vanish (the "dot-product attention problem").

---

## Numerical Stability

Naive softmax overflows with large logits.  Stable implementation:

```python
def softmax(z):
    z = z - z.max()          # subtract max for numerical stability
    return z.exp() / z.exp().sum()
```

PyTorch's `F.softmax` handles this internally.

---

## Karpathy Resources

- makemore Part 1 — first use of softmax for bigram probs
- Let's build GPT — scaled dot-product attention softmax
