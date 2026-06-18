# LLM — Large Language Model

> **Tags:** #core #overview
> **Related:** [[Transformer]], [[GPT]], [[Training]], [[Tokenization]]

---

## What Is a Large Language Model?

A **Large Language Model (LLM)** is a [[Neural-Network]] trained on massive amounts of text to predict the next token in a sequence.  Once trained, the model learns statistical patterns of language that encode world knowledge, reasoning, and style.

```
Input tokens → [LLM] → Probability distribution over next token
```

The "large" refers to parameter count — modern LLMs range from billions to trillions of parameters.

---

## Key Stages

### 1. Pre-training
The model is trained on a huge corpus (internet text, books, code) with a simple **next-token prediction** objective.  See [[Training]] and [[Loss-Function]].

### 2. Fine-tuning / Instruction Tuning
The pre-trained model is further trained on curated instruction-following data to make it helpful and safe.

### 3. RLHF (Reinforcement Learning from Human Feedback)
Human preferences are used to train a reward model; the LLM is then optimised against this reward via PPO or similar algorithms.

---

## The Core Loop

```
for each training step:
    sample context window of tokens       # [[Tokenization]]
    forward pass through [[Transformer]]  # [[Attention]] + [[MLP]]
    compute [[Loss-Function]]             # cross-entropy
    [[Backpropagation]]                   # compute gradients
    [[Training|optimiser step]]           # update weights
```

---

## Emergent Capabilities

As scale increases, LLMs exhibit emergent abilities:
- In-context learning (few-shot prompting)
- Chain-of-thought reasoning
- Code generation
- Instruction following

---

## Key Karpathy Quote

> "The neural network is not just a language model; it is a general-purpose simulator of a person who has read all of the internet."
> — Andrej Karpathy, *State of GPT* (2023)

---

## Resources

- [State of GPT (2023) — Karpathy](https://youtu.be/bZQun8Y4L2A)
- [nanoGPT](https://github.com/karpathy/nanoGPT)
- [llm.c](https://github.com/karpathy/llm.c)
