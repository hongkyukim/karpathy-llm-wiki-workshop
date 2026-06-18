# Backpropagation

> **Tags:** #training #foundation
> **Related:** [[Training]], [[Neural-Network]], [[Loss-Function]], [[MLP]]

---

## What Is Backpropagation?

**Backpropagation** is the algorithm that computes the **gradient** of the [[Loss-Function]] with respect to every parameter in the [[Neural-Network]].  It is an efficient application of the **chain rule** of calculus, working backwards from the loss through the computation graph.

```
∂L/∂W  =  ∂L/∂z  ·  ∂z/∂W
```

---

## Intuition

Think of each operation in the forward pass as a node in a directed acyclic graph (DAG):

```
W, x  →  [matmul]  →  z  →  [tanh]  →  a  →  [linear]  →  logits  →  [cross-entropy]  →  loss
```

Backprop traverses this graph **right to left**, computing and accumulating partial derivatives.

---

## The Chain Rule in Practice

For a composition `L = f(g(x))`:

```
dL/dx = (dL/df) * (df/dg) * (dg/dx)
```

In a neural network every operation (matmul, add, tanh, ReLU) knows its own local derivative.

---

## Manual Backprop (Karpathy makemore Part 3–5)

Karpathy famously walks through computing all gradients *by hand* — without `loss.backward()` — to build intuition:

```python
# forward
logit_maxes  = logits.max(1, keepdim=True).values
norm_logits  = logits - logit_maxes
counts       = norm_logits.exp()
counts_sum   = counts.sum(1, keepdim=True)
probs        = counts / counts_sum
logprobs     = probs.log()
loss         = -logprobs[range(n), Yb].mean()

# backward (manual)
dlogprobs = torch.zeros_like(logprobs)
dlogprobs[range(n), Yb] = -1.0 / n
dprobs     = dlogprobs / probs
# ... (continues for every node)
```

---

## Automatic Differentiation

PyTorch's **autograd** engine does this automatically when `.backward()` is called.  Understanding manual backprop helps debug NaN gradients, exploding/vanishing gradients, and dead neurons.

---

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Vanishing gradients | Deep tanh / sigmoid | Use ReLU, residual connections |
| Exploding gradients | Large weights | Gradient clipping |
| Dead ReLU | Negative pre-activations | Careful initialisation |

---

## Karpathy Resources

- micrograd — [GitHub](https://github.com/karpathy/micrograd) — builds autograd from scratch
- makemore Part 3 — activations, gradients, BatchNorm
- makemore Part 4 — manual backprop "from scratch"
