# Aether-XAI

> **A multi-tenant neuro-symbolic AI engine that combines deep learning, formal verification, and explainable AI for secure enterprise inference.**

[![CI Pipeline](https://github.com/USERNAME/aether-xai/actions/workflows/ci.yml/badge.svg)](https://github.com/USERNAME/aether-xai/actions)

Aether-XAI is designed for production environments where AI decisions need to be **accurate, explainable, and verifiable**. It combines a PyTorch neural network with symbolic reasoning using the Z3 SMT solver while enforcing strict tenant isolation through PostgreSQL Row-Level Security (RLS).

---

# Architecture

```text
Incoming Request
        │
        ▼
Tenant Context Middleware
        │
        ▼
PyTorch Neural Network
        │
        ▼
Z3 Symbolic Verification
        │
        ▼
Explainability Engine
      (SHAP)
        │
        ▼
PostgreSQL (Row-Level Security)
```

---

# How It Works

1. A request enters through the tenant middleware, which identifies and validates the active tenant.
2. The neural model generates a probabilistic risk score.
3. The prediction is validated against tenant-specific rules using the Z3 SMT solver.
4. Feature importance is generated to explain the prediction.
5. Results are stored securely using PostgreSQL Row-Level Security to ensure complete tenant isolation.

---

# Mathematical Model

### Neural Risk Prediction

The neural network maps an input feature vector **x** to a probability score between 0 and 1.

[
\hat{y}=\sigma\left(W_L\cdot\text{ReLU}\left(\cdots\text{ReLU}(W_1x+b_1)\cdots\right)+b_L\right)
]

where

[
\sigma(z)=\frac{1}{1+e^{-z}}
]

---

### Symbolic Verification

Each prediction is checked against a tenant-defined threshold using the Z3 SMT solver.

[
\phi=(risk=\hat{y})\land(risk\le\tau)
]

Decision rule:

[
Decision(\hat{y},\tau)=
\begin{cases}
\textbf{ACCEPT}, & \mathcal{M}\models\phi \
\textbf{REJECT}, & \text{otherwise}
\end{cases}
]

---

### Feature Attribution

Feature importance is computed using normalized absolute contribution.

[
w_i=\frac{|x_i|}{\sum_{j=1}^{d}|x_j|+\epsilon}
]

where

[
\epsilon=10^{-9}
]

---

# Key Features

* **Multi-Tenant Architecture** — Secure tenant isolation using PostgreSQL Row-Level Security (RLS).
* **Neuro-Symbolic Inference** — Combines probabilistic neural networks with symbolic reasoning.
* **Formal Verification** — Policy validation powered by the Z3 SMT solver.
* **Explainable AI** — Feature attribution and confidence metrics for every prediction.
* **FastAPI Backend** — High-performance asynchronous REST API.
* **Production Ready** — Modular architecture with CI support and enterprise deployment in mind.

---

# Tech Stack

| Component          | Technology                          |
| ------------------ | ----------------------------------- |
| API                | FastAPI                             |
| Machine Learning   | PyTorch                             |
| Symbolic Reasoning | Z3 SMT Solver                       |
| Explainability     | SHAP                                |
| Database           | PostgreSQL                          |
| Security           | PostgreSQL Row-Level Security (RLS) |
| ORM                | SQLAlchemy                          |
| Validation         | Pydantic                            |
| Deployment         | Docker                              |

---

## Project Goal

Aether-XAI demonstrates how neural networks and symbolic reasoning can work together to produce AI systems that are not only accurate, but also transparent, verifiable, and secure for multi-tenant enterprise applications.
