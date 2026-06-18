# 🧠 Karpathy LLM Wiki — Index

> A structured knowledge base for Andrej Karpathy's LLM lecture series.
> Open this folder as an **Obsidian vault** to explore the Graph View.

---

## Learning Path (Recommended Order)

1. [[Neural-Network]] — universal function approximators
2. [[Bigram-Model]] — the simplest possible language model
3. [[MLP]] — adding hidden layers & learning representations
4. [[Embedding]] — turning tokens into dense vectors
5. [[Softmax]] — converting raw scores to probabilities
6. [[Loss-Function]] — measuring how wrong we are
7. [[Backpropagation]] — computing gradients efficiently
8. [[Training]] — gradient descent, optimisers, schedules
9. [[Tokenization]] — converting text ↔ token IDs
10. [[Attention]] — letting tokens communicate
11. [[Transformer]] — stacking attention + MLP blocks
12. [[GPT]] — the full GPT architecture
13. [[LLM]] — pre-training, fine-tuning, and beyond

---

## Concept Map

```
Neural-Network
  └─► MLP
        └─► Embedding ──► Transformer ──► GPT ──► LLM
                              │
                         Attention
                              │
                         Softmax
Bigram-Model ──► MLP
Loss-Function ◄── (all models)
Backpropagation ◄── Training
Tokenization ──► Embedding
```

---

## Karpathy Video Series

| Video | Key Concepts |
|-------|-------------|
| makemore Part 1 | [[Bigram-Model]], [[Loss-Function]] |
| makemore Part 2 | [[MLP]], [[Embedding]] |
| makemore Part 3–5 | [[Backpropagation]], [[Training]] |
| Let's build GPT | [[Transformer]], [[Attention]], [[GPT]] |
| GPT Tokenizer | [[Tokenization]] |
| State of GPT | [[LLM]], [[Training]] |
