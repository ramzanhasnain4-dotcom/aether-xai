# Aether-XAI

A research project exploring how neural networks and symbolic reasoning can be combined to build more reliable AI systems.

The project uses a PyTorch model for prediction, validates outputs with the Z3 SMT solver, and stores tenant data securely using PostgreSQL Row-Level Security (RLS).

---

## Overview

```text
Client Request
      │
      ▼
Tenant Middleware
      │
      ▼
PyTorch Model
      │
      ▼
Z3 Verification
      │
      ▼
SHAP Explanation
      │
      ▼
PostgreSQL (RLS)
```

---

## How it works

1. A request enters the API with tenant information.
2. The neural network predicts a risk score.
3. The prediction is checked against tenant-specific constraints using Z3.
4. SHAP generates feature importance values.
5. The prediction and explanation are stored in PostgreSQL under the correct tenant.

---

## Mathematical Model

The prediction network is defined as

[
\hat{y}=\sigma\left(W_L(\mathrm{ReLU}(\cdots\mathrm{ReLU}(W_1x+b_1)))+b_L\right)
]

where (\sigma) is the sigmoid activation function.

The symbolic constraint is

[
(risk=\hat{y}) \land (risk \le \tau)
]

If the constraint is satisfiable, the prediction is accepted; otherwise it is rejected.

Feature importance is calculated as

[
w_i=\frac{|x_i|}{\sum_j |x_j|+\epsilon}
]

---

## Features

* Multi-tenant inference
* PostgreSQL Row-Level Security
* PyTorch prediction model
* Z3 SMT-based policy verification
* SHAP feature attribution
* FastAPI REST API
* Docker support

---

## Project Structure

```text
api/
core/
models/
services/
tests/
benchmarks/
```

---

## Running the project

Clone the repository.

```bash
git clone https://github.com/USERNAME/aether-xai.git
cd aether-xai
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Start the API.

```bash
uvicorn api.main:app --reload
```

Run tests.

```bash
pytest tests/
```

Run the benchmark.

```bash
python benchmarks/latency_test.py
```

---

## Notes

This project was built to experiment with combining statistical learning and symbolic reasoning in a multi-tenant backend. The implementation focuses on keeping the components modular so different neural models, verification rules, or explanation methods can be swapped with minimal changes.
