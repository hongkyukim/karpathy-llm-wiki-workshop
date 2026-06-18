# Tokenization

> **Tags:** #preprocessing
> **Related:** [[LLM]], [[Embedding]], [[GPT]], [[Transformer]]

---

## What Is Tokenization?

**Tokenization** converts raw text (a sequence of Unicode characters) into a sequence of integer **token IDs** that the model processes.  It is the very first step in the LLM pipeline.

```
"Hello, world!"  →  tokenizer  →  [15496, 11, 995, 0]
```

---

## Why Not Characters?

| Approach | Vocabulary | Context efficiency | Problem |
|----------|-----------|-------------------|---------|
| Character-level | ~100–300 | Low (long sequences) | Poor for long-range dependencies |
| Word-level | ~50 000+ | High | Fails on rare/unknown words |
| **Sub-word (BPE)** | ~32 000–100 000 | Balanced | ✅ Best of both worlds |

---

## Byte-Pair Encoding (BPE)

**BPE** is the algorithm used by GPT-2/GPT-4 tokenizers.

**Algorithm:**
1. Start with individual bytes (256 base tokens).
2. Count the most frequent pair of adjacent tokens.
3. Merge that pair into a new single token.
4. Repeat until vocabulary reaches target size.

```python
# Simplified BPE merge step
def get_stats(ids):
    pairs = {}
    for pair in zip(ids, ids[1:]):
        pairs[pair] = pairs.get(pair, 0) + 1
    return pairs

def merge(ids, pair, idx):
    new_ids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and (ids[i], ids[i+1]) == pair:
            new_ids.append(idx)
            i += 2
        else:
            new_ids.append(ids[i])
            i += 1
    return new_ids
```

---

## Special Tokens

| Token | Meaning |
|-------|---------|
| `<|endoftext|>` | End of document (GPT-2/3/4) |
| `<|im_start|>` | Conversation turn start (ChatML) |
| `[BOS]`, `[EOS]` | Beginning/end of sequence |

---

## Token Count ≠ Character Count

```
"Hello"              → 1 token
"Antidisestablishmentarianism" → 6 tokens
" python"            → 2 tokens  (note: space matters!)
```

This has practical consequences:
- API costs are per token.
- Context windows are measured in tokens.
- Prompt engineering is partly token engineering.

---

## Tokenizer Libraries

```python
import tiktoken
enc = tiktoken.get_encoding("gpt2")
enc.encode("Hello, world!")   # [15496, 11, 995, 0]
enc.decode([15496, 11])       # "Hello,"
```

---

## Karpathy Resources

- [Let's build the GPT Tokenizer (YouTube)](https://youtu.be/zduSFxRajkE) — 2-hour deep dive
- [minbpe](https://github.com/karpathy/minbpe) — minimal BPE tokenizer in Python
