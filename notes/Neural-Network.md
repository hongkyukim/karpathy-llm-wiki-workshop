# Neural Network

> **Tags:** #foundation
> **Related:** [[MLP]], [[Backpropagation]], [[Training]], [[Loss-Function]]

---

## What Is a Neural Network?

A **neural network** is a parametric function f(x; θ) composed of layers of simple operations (linear transformations + non-linear activations) that can approximate any continuous function given enough parameters.

```
x ──► [Linear] ──► [Activation] ──► [Linear] ──► [Activation] ──► y_hat
```

---

## Core Components

| Component | Description |
|-----------|-------------|
| **Neuron** | Takes a weighted sum of inputs, adds a bias, applies an activation |
| **Layer** | A collection of neurons operating in parallel |
| **Weight (W)** | Learnable matrix multiplied by the input |
| **Bias (b)** | Learnable offset added after the matrix multiply |
| **Activation** | Non-linear function (ReLU, tanh, GELU) applied element-wise |

---

## Forward Pass

For a single layer with input **x**, weight **W**, bias **b**:

```
z = W @ x + b      # linear part
a = activation(z)  # non-linear part
```

Stacking multiple layers gives a **deep** neural network (→ [[MLP]]).

---

## Learning

- The network is wrong at first — it starts with random weights.
- We measure how wrong it is with a [[Loss-Function]].
- [[Backpropagation]] computes the gradient of the loss w.r.t. every weight.
- [[Training|Gradient descent]] updates weights to reduce the loss.

---

## Why Depth Matters

Deeper networks can represent exponentially more complex functions than shallow ones with the same total number of parameters.  Each layer builds representations from the previous layer's output.

---

## Karpathy Resources

- [micrograd](https://github.com/karpathy/micrograd) — tiny autograd engine (100 lines)
- makemore Part 1 — builds the first neural network from scratch
