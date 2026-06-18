# GPT — Generative Pre-trained Transformer

> **Tags:** #architecture #model
> **Related:** [[Transformer]], [[Attention]], [[Embedding]], [[Tokenization]], [[Training]], [[LLM]]

---

## What Is GPT?

**GPT** (Generative Pre-trained Transformer) is a **decoder-only [[Transformer]]** trained with **next-token prediction** on large text corpora.

The family spans:
| Model | Parameters | Year |
|-------|-----------|------|
| GPT-1 | 117M | 2018 |
| GPT-2 | 1.5B | 2019 |
| GPT-3 | 175B | 2020 |
| GPT-4 | ~1T (est.) | 2023 |

---

## Model Architecture (nanoGPT)

```python
class GPT(nn.Module):
    def __init__(self, config):
        self.transformer = nn.ModuleDict(dict(
            wte  = nn.Embedding(config.vocab_size, config.n_embd),   # token emb
            wpe  = nn.Embedding(config.block_size, config.n_embd),   # position emb
            drop = nn.Dropout(config.dropout),
            h    = nn.ModuleList([Block(config) for _ in range(config.n_layer)]),
            ln_f = nn.LayerNorm(config.n_embd),
        ))
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
```

Each `Block` contains:
1. `LayerNorm` → `CausalSelfAttention` → `+ residual`
2. `LayerNorm` → `MLP (FFN)` → `+ residual`

---

## Forward Pass

```
tokens (B, T)
  → token_emb (B, T, C)  +  pos_emb (T, C)
  → N × [attention + MLP] blocks
  → LayerNorm
  → lm_head  →  logits (B, T, vocab_size)
  → cross_entropy(logits, targets)  →  loss
```

---

## Inference (Text Generation)

```python
for _ in range(max_new_tokens):
    logits = model(idx[:, -block_size:])  # trim to context window
    logits = logits[:, -1, :]             # last token position
    probs  = F.softmax(logits / temperature, dim=-1)
    idx_next = torch.multinomial(probs, num_samples=1)
    idx = torch.cat([idx, idx_next], dim=1)
```

---

## GPT-2 Configuration (Small)

```python
@dataclass
class GPTConfig:
    block_size: int = 1024   # context window
    vocab_size: int = 50257  # BPE vocabulary
    n_layer:    int = 12     # transformer layers
    n_head:     int = 12     # attention heads
    n_embd:     int = 768    # embedding dimension
```

---

## Pre-training → Fine-tuning Pipeline

```
Raw text corpus
  → [[Tokenization]] (BPE, 50k vocab)
  → Pre-training (predict next token, ~300B tokens)
  → Instruction fine-tuning (supervised, instruction pairs)
  → RLHF (reward model + PPO)
  → InstructGPT / ChatGPT
```

---

## Karpathy Resources

- Let's build GPT — [YouTube](https://youtu.be/kCc8FmEb1nY)
- [nanoGPT](https://github.com/karpathy/nanoGPT)
- State of GPT (2023) — [YouTube](https://youtu.be/bZQun8Y4L2A)
