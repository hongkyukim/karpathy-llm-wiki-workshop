# Training

> **Tags:** #training
> **Related:** [[Backpropagation]], [[Loss-Function]], [[Neural-Network]], [[LLM]], [[GPT]]

---

## What Is Training?

**Training** is the iterative process of adjusting model parameters (weights) to minimise the [[Loss-Function]].

```
repeat:
    1. Sample a mini-batch of data
    2. Forward pass  →  compute predictions & loss
    3. [[Backpropagation]]  →  compute gradients
    4. Optimiser step  →  update weights
    5. Zero gradients
```

---

## Gradient Descent Variants

| Variant | Description |
|---------|------------|
| **SGD** | Update once per single example |
| **Mini-batch SGD** | Update once per batch (B samples) |
| **Adam** | Adaptive per-parameter learning rates |
| **AdamW** | Adam + decoupled weight decay (preferred for [[LLM]]) |

```python
optimiser = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.1)
```

---

## Learning Rate

The learning rate (lr) controls how large each update step is.

- Too high → loss explodes or oscillates.
- Too low → training is slow or stalls.
- Typical starting value: **3e-4** (Karpathy's recommended "golden number").

### Learning Rate Schedule (nanoGPT)

```
warmup (linear 0 → max_lr)
  →  cosine decay (max_lr → min_lr)
```

---

## Overfitting vs. Underfitting

| Symptom | Training loss | Validation loss |
|---------|--------------|-----------------|
| Underfitting | High | High |
| Good fit | Low | Low |
| Overfitting | Low | High |

Fixes for overfitting: dropout, weight decay, more data, smaller model.

---

## Batch Size

- Larger batches → more stable gradients, but slower iterations.
- Typical: 32–512 for character-level models; 0.5M tokens per batch for [[GPT]]-scale training.

---

## Key Hyperparameters (nanoGPT)

```python
batch_size     = 64
block_size     = 256        # context window
max_iters      = 5000
eval_interval  = 500
learning_rate  = 3e-4
n_embd         = 384
n_head         = 6
n_layer        = 6
dropout        = 0.2
```

---

## Karpathy Resources

- makemore Part 5 — WaveNet & training tricks
- Let's build GPT — training nanoGPT end-to-end
- [nanoGPT train.py](https://github.com/karpathy/nanoGPT/blob/master/train.py)
