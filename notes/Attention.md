# Attention — Self-Attention Mechanism

> **Tags:** #architecture #transformer
> **Related:** [[Transformer]], [[Embedding]], [[Softmax]], [[GPT]], [[MLP]]

---

## What Is Self-Attention?

**Self-attention** allows every token in a sequence to *attend to* (look at and aggregate information from) every other token.  It is the core innovation of the [[Transformer]].

```
Each token asks:  "Which other tokens are relevant to me?"
```

Unlike RNNs, attention processes all tokens in **parallel** and captures long-range dependencies directly.

---

## Query, Key, Value

Each token projects itself into three vectors:

| Vector | Role | Analogy |
|--------|------|---------|
| **Q** (Query) | "What am I looking for?" | A search query |
| **K** (Key) | "What do I contain?" | A database key |
| **V** (Value) | "What do I return?" | A database value |

```
Q = x @ W_Q    # (T, d_k)
K = x @ W_K    # (T, d_k)
V = x @ W_V    # (T, d_v)
```

---

## Scaled Dot-Product Attention

```
Attention(Q, K, V) = softmax( Q @ K.T / sqrt(d_k) ) @ V
```

1. **Q @ K.T** — compute pairwise similarity scores  `(T × T)`
2. **/ sqrt(d_k)** — scale to prevent vanishing gradients
3. **softmax(...)** — convert scores to probabilities (each row sums to 1)
4. **@ V** — weighted sum of value vectors

---

## Causal (Masked) Attention

For auto-regressive language modelling (predict next token), future tokens must be **masked**:

```python
mask = torch.tril(torch.ones(T, T))    # lower-triangular
att  = att.masked_fill(mask == 0, float('-inf'))
att  = F.softmax(att, dim=-1)
```

---

## Multi-Head Attention

Run `h` independent attention heads in parallel, then concatenate:

```
MultiHead(Q,K,V) = concat(head_1, ..., head_h) @ W_O

where head_i = Attention(Q @ W_Qi, K @ W_Ki, V @ W_Vi)
```

Each head can focus on different types of relationships (syntactic, semantic, positional).

---

## Karpathy's nanoGPT Implementation

```python
class CausalSelfAttention(nn.Module):
    def forward(self, x):
        B, T, C = x.size()
        q, k, v = self.c_attn(x).split(self.n_embd, dim=2)
        # reshape to (B, n_head, T, head_size)
        ...
        att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
        att = att.masked_fill(self.bias[:,:,:T,:T] == 0, float('-inf'))
        att = F.softmax(att, dim=-1)
        y = att @ v
        return self.c_proj(y)
```

---

## Karpathy Resources

- Let's build GPT — [YouTube](https://youtu.be/kCc8FmEb1nY) — attention explained from scratch
- "Attention Is All You Need" paper (Vaswani et al., 2017)
