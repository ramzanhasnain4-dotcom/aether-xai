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

## How the Model Works

### Prediction

The neural network is a standard feed-forward model. Input features pass through multiple hidden layers, each applying a linear transformation followed by a ReLU activation. The final layer uses a **sigmoid** function to output a risk score between 0 and 1.

### Verification

After the model produces a risk score, the Z3 solver checks it against tenant-specific rules — for example, *"the risk score must not exceed the tenant's threshold."* If the score passes, the prediction is accepted. If it violates any constraint, the prediction is rejected.

### Feature Importance

SHAP (SHapley Additive exPlanations) is used to explain predictions. Each input feature gets an importance weight based on how much it contributed to the model's output, making the results interpretable.

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
git clone https://github.com/ramzanhasnain4-dotcom/aether-xai.git
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

---

## Running with Docker

The easiest way to get everything running is with Docker Compose. This spins up both the **API** and a **PostgreSQL 16** database with the schema auto-applied.

```bash
docker-compose up --build
```

This will:

* Build the `aether_api` container from the Dockerfile
* Start a `aether_db` Postgres container with RLS schema applied from `schema/`
* Connect the API to the database automatically
* Expose the API at `http://localhost:8000`

To run in detached mode:

```bash
docker-compose up --build -d
```

To stop everything:

```bash
docker-compose down
```

### Running just the API container (no Compose)

If you already have a Postgres instance running elsewhere, you can build and run the API container on its own:

```bash
docker build -t aether-xai .
docker run -p 8000:8000 -e DATABASE_URL=postgresql://user:pass@host:5432/aether_xai aether-xai
```

Replace the `DATABASE_URL` value with your actual database connection string.

---

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
