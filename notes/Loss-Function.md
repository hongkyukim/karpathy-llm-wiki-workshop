# Loss Function

> **Tags:** #training #foundation
> **Related:** [[Training]], [[Backpropagation]], [[Softmax]], [[Neural-Network]], [[LLM]]

---

## What Is a Loss Function?

A **loss function** (also called a **cost function** or **objective**) measures how wrong the model's predictions are.  Training is the process of minimising this number.

```
loss = L(y_hat, y_true)
```

A low loss means good predictions; a high loss means bad predictions.

---

## Cross-Entropy Loss (for Language Models)

Language models use **negative log-likelihood / cross-entropy**:

```
loss = −  (1/N) Σ_i  log P(correct_token_i)
```

Intuitively: penalise the model more the lower it rates the correct answer.

```python
loss = F.cross_entropy(logits, targets)
# logits: (B*T, vocab_size)  targets: (B*T,)
```

`F.cross_entropy` = softmax + negative log-likelihood in one numerically stable call.

---

## Perplexity

**Perplexity** is the exponentiated cross-entropy loss:

```
perplexity = exp(loss)
```

It has an intuitive interpretation: "how many equally likely next tokens does the model consider on average?"  A perfectly uniform model over a 27-character vocabulary has perplexity = 27.

| Stage | Typical Character-Level Perplexity |
|-------|----------------------------------|
| Random init | ~27 (for 27-char vocab) |
| Bigram model | ~2.1 |
| MLP | ~1.7 |
| Transformer | ~1.5 and below |

---

## Regularisation in Loss

Karpathy adds **L2 regularisation** (weight decay) in some examples:

```python
loss = cross_entropy_loss + lambda * sum(p**2 for p in model.parameters())
```

Modern frameworks handle this via the `weight_decay` argument in optimisers like AdamW.

---

## Other Losses (Advanced)

| Loss | Use case |
|------|---------|
| Cross-entropy | Pre-training language models |
| KL divergence | Distillation, RLHF reference penalty |
| Reward signal | RLHF policy gradient |

---

## Karpathy Resources

- makemore Part 1 — NLL loss from scratch
- Let's build GPT — `F.cross_entropy` in nanoGPT
