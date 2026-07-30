"""
Aether-XAI Benchmark Suite
Generates performance graphs for README documentation.
Run: python benchmarks/generate_graphs.py
"""

import time
import os
import sys
import numpy as np
import torch

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.neural_model import load_pretrained_model
from core.symbolic_verifier import SymbolicGuardrail
from core.explainability import XAIEngine

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as ticker
except ImportError:
    print("matplotlib is required. Install with: pip install matplotlib")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
COLORS = {
    "primary":    "#6C5CE7",
    "secondary":  "#00CEC9",
    "accent":     "#FD79A8",
    "warning":    "#FDCB6E",
    "bg":         "#0F0F1A",
    "card":       "#1A1A2E",
    "grid":       "#2D2D44",
    "text":       "#E0E0E0",
}

plt.rcParams.update({
    "figure.facecolor":  COLORS["bg"],
    "axes.facecolor":    COLORS["card"],
    "axes.edgecolor":    COLORS["grid"],
    "axes.labelcolor":   COLORS["text"],
    "text.color":        COLORS["text"],
    "xtick.color":       COLORS["text"],
    "ytick.color":       COLORS["text"],
    "grid.color":        COLORS["grid"],
    "grid.alpha":        0.3,
    "font.family":       "sans-serif",
    "font.size":         11,
})

OUT_DIR = os.path.join(os.path.dirname(__file__), "graphs")
os.makedirs(OUT_DIR, exist_ok=True)


# ---------------------------------------------------------------------------
# 1. Z3 Verification Latency Distribution
# ---------------------------------------------------------------------------
def bench_z3_latency(runs: int = 500) -> list[float]:
    verifier = SymbolicGuardrail(max_allowed_risk=0.75)
    latencies = []
    for i in range(runs):
        risk = (i % 100) / 100.0
        t0 = time.perf_counter()
        verifier.verify_prediction(risk)
        latencies.append((time.perf_counter() - t0) * 1000)
    return latencies


def plot_z3_latency(latencies: list[float]):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.hist(latencies, bins=40, color=COLORS["primary"], edgecolor=COLORS["bg"],
            alpha=0.85, linewidth=0.5)

    mean_lat = np.mean(latencies)
    p99_lat  = np.percentile(latencies, 99)
    ax.axvline(mean_lat, color=COLORS["secondary"], linestyle="--", linewidth=1.5,
               label=f"Mean  {mean_lat:.2f} ms")
    ax.axvline(p99_lat, color=COLORS["accent"], linestyle="--", linewidth=1.5,
               label=f"P99   {p99_lat:.2f} ms")

    ax.set_xlabel("Latency (ms)")
    ax.set_ylabel("Frequency")
    ax.set_title("Z3 SMT Verification Latency Distribution", fontweight="bold", fontsize=13)
    ax.legend(frameon=False)
    ax.grid(True, axis="y")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "z3_latency.png"), dpi=180)
    plt.close(fig)
    print(f"  [OK] Z3 latency -- mean={mean_lat:.2f} ms | p99={p99_lat:.2f} ms")


# ---------------------------------------------------------------------------
# 2. Neural Inference Throughput (batch scaling)
# ---------------------------------------------------------------------------
def bench_inference_throughput() -> tuple[list[int], list[float]]:
    model = load_pretrained_model()
    batch_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    throughputs = []
    for bs in batch_sizes:
        x = torch.randn(bs, 5)
        # warm-up
        with torch.no_grad():
            model(x)
        t0 = time.perf_counter()
        reps = 200
        for _ in range(reps):
            with torch.no_grad():
                model(x)
        elapsed = time.perf_counter() - t0
        throughputs.append((bs * reps) / elapsed)
    return batch_sizes, throughputs


def plot_inference_throughput(batch_sizes, throughputs):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(batch_sizes, throughputs, marker="o", color=COLORS["secondary"],
            linewidth=2, markersize=7, markerfacecolor=COLORS["primary"],
            markeredgecolor=COLORS["secondary"])
    ax.fill_between(batch_sizes, throughputs, alpha=0.10, color=COLORS["secondary"])
    ax.set_xlabel("Batch Size")
    ax.set_ylabel("Throughput (inferences / sec)")
    ax.set_title("Neural Model Inference Throughput", fontweight="bold", fontsize=13)
    ax.set_xscale("log", base=2)
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "inference_throughput.png"), dpi=180)
    plt.close(fig)
    peak = max(throughputs)
    print(f"  [OK] Inference throughput -- peak={peak:,.0f} inf/s @ batch {batch_sizes[throughputs.index(peak)]}")


# ---------------------------------------------------------------------------
# 3. End-to-End Pipeline Latency Breakdown
# ---------------------------------------------------------------------------
def bench_pipeline_breakdown(runs: int = 300) -> dict[str, float]:
    model = load_pretrained_model()
    verifier = SymbolicGuardrail(max_allowed_risk=0.75)
    xai = XAIEngine(feature_names=["f1", "f2", "f3", "f4", "f5"])

    times = {"Neural Inference": [], "Z3 Verification": [], "XAI Attribution": []}
    for _ in range(runs):
        x = torch.randn(1, 5)

        t0 = time.perf_counter()
        with torch.no_grad():
            pred = float(model(x).squeeze().item())
        times["Neural Inference"].append((time.perf_counter() - t0) * 1000)

        t0 = time.perf_counter()
        verifier.verify_prediction(pred)
        times["Z3 Verification"].append((time.perf_counter() - t0) * 1000)

        t0 = time.perf_counter()
        xai.compute_attributions([0.1, 0.2, 0.3, 0.4, 0.5])
        times["XAI Attribution"].append((time.perf_counter() - t0) * 1000)

    return {k: np.mean(v) for k, v in times.items()}


def plot_pipeline_breakdown(breakdown: dict[str, float]):
    labels = list(breakdown.keys())
    values = list(breakdown.values())
    colors = [COLORS["primary"], COLORS["secondary"], COLORS["accent"]]

    fig, ax = plt.subplots(figsize=(9, 4.5))
    bars = ax.barh(labels, values, color=colors, edgecolor=COLORS["bg"], height=0.5)

    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + max(values) * 0.02, bar.get_y() + bar.get_height() / 2,
                f"{val:.3f} ms", va="center", fontsize=10, color=COLORS["text"])

    ax.set_xlabel("Average Latency (ms)")
    ax.set_title("Pipeline Stage Latency Breakdown", fontweight="bold", fontsize=13)
    ax.invert_yaxis()
    ax.grid(True, axis="x")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "pipeline_breakdown.png"), dpi=180)
    plt.close(fig)
    total = sum(values)
    print(f"  [OK] Pipeline breakdown -- total={total:.3f} ms")


# ---------------------------------------------------------------------------
# 4. Multi-Tenant Concurrent Scaling
# ---------------------------------------------------------------------------
def bench_tenant_scaling() -> tuple[list[int], list[float], list[float]]:
    model = load_pretrained_model()
    tenant_counts = [1, 2, 4, 8, 16, 32]
    avg_latencies = []
    p99_latencies = []

    for n_tenants in tenant_counts:
        latencies = []
        for t in range(n_tenants):
            verifier = SymbolicGuardrail(max_allowed_risk=round(0.5 + (t % 5) * 0.1, 2))
            x = torch.randn(1, 5)
            t0 = time.perf_counter()
            with torch.no_grad():
                pred = float(model(x).squeeze().item())
            verifier.verify_prediction(pred)
            latencies.append((time.perf_counter() - t0) * 1000)
        avg_latencies.append(np.mean(latencies))
        p99_latencies.append(np.percentile(latencies, 99))

    return tenant_counts, avg_latencies, p99_latencies


def plot_tenant_scaling(tenant_counts, avg_latencies, p99_latencies):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(tenant_counts, avg_latencies, marker="s", color=COLORS["secondary"],
            linewidth=2, label="Mean Latency", markersize=7)
    ax.plot(tenant_counts, p99_latencies, marker="^", color=COLORS["accent"],
            linewidth=2, label="P99 Latency", markersize=7)
    ax.fill_between(tenant_counts, avg_latencies, p99_latencies,
                    alpha=0.08, color=COLORS["accent"])

    ax.set_xlabel("Concurrent Tenants")
    ax.set_ylabel("Latency (ms)")
    ax.set_title("Multi-Tenant Scaling: Latency vs Tenant Count",
                 fontweight="bold", fontsize=13)
    ax.legend(frameon=False)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "tenant_scaling.png"), dpi=180)
    plt.close(fig)
    print(f"  [OK] Tenant scaling  --  32 tenants avg={avg_latencies[-1]:.3f} ms")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def main():
    print("\n  Aether-XAI Benchmark Suite")
    print("  " + "=" * 40)

    print("\n  Running Z3 verification latency benchmark ...")
    lat = bench_z3_latency()
    plot_z3_latency(lat)

    print("  Running inference throughput benchmark ...")
    bs, tp = bench_inference_throughput()
    plot_inference_throughput(bs, tp)

    print("  Running pipeline breakdown benchmark ...")
    bd = bench_pipeline_breakdown()
    plot_pipeline_breakdown(bd)

    print("  Running tenant scaling benchmark ...")
    tc, al, pl = bench_tenant_scaling()
    plot_tenant_scaling(tc, al, pl)

    print(f"\n  All graphs saved to: {OUT_DIR}/")
    print("  " + "=" * 40 + "\n")


if __name__ == "__main__":
    main()
