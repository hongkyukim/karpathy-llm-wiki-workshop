# Bigram Model

> **Tags:** #language-model #foundation
> **Related:** [[Neural-Network]], [[LLM]], [[Loss-Function]], [[Tokenization]], [[Training]]

---

## What Is a Bigram Model?

A **bigram language model** predicts the next character (or token) using *only* the immediately preceding character.

```
P(next token | context) ≈ P(next token | previous token)
```

It is the simplest possible [[LLM]] — a single lookup table of counts.

---

## Character-Level Bigram (Karpathy makemore Part 1)

Karpathy builds this in `makemore` by:

1. Counting all bigram pairs in a dataset of names.
2. Normalising each row to obtain conditional probabilities.
3. Sampling new names by repeatedly drawing from these distributions.

```python
# Count bigrams
N = torch.zeros((27, 27), dtype=torch.int32)
for word in words:
    chs = ['.'] + list(word) + ['.']
    for ch1, ch2 in zip(chs, chs[1:]):
        N[stoi[ch1], stoi[ch2]] += 1

# Normalise to probabilities
P = N.float()
P /= P.sum(dim=1, keepdim=True)
```

---

## From Counts to Neural Network

The same bigram model can be expressed as a one-layer [[Neural-Network]]:

```
one-hot(xenc) @ W  →  logits  →  [[Softmax]]  →  probs
```

The weight matrix **W** learns the same values as the count table (up to a log transform).  This reformulation makes it easy to extend to deeper models (→ [[MLP]]).

---

## Limitations

| Limitation | Fix |
|-----------|-----|
| Only uses 1 token of context | Use longer context → [[MLP]], [[Transformer]] |
| No shared representations | Use [[Embedding]] layers |
| Hard to scale | Replace with deep [[Neural-Network]] |

---

## Loss

The model is trained with **negative log-likelihood** (→ [[Loss-Function]]):

```
loss = -mean(log P(actual_next_token))
```

---

## Karpathy Resources

- makemore Part 1 — [YouTube](https://youtu.be/PaCmpygFfXo)
- makemore source — [GitHub](https://github.com/karpathy/makemore)
