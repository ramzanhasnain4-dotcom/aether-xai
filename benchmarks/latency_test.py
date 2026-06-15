import time
from core.symbolic_verifier import SymbolicGuardrail

def run_latency_benchmark(num_runs: int = 1000):
    """Measures average latency of Z3 SMT constraint checking across 1000 iterations."""
    verifier = SymbolicGuardrail(max_allowed_risk=0.75)
    start_time = time.perf_counter()
    
    for i in range(num_runs):
        risk_val = (i % 100) / 100.0
        verifier.verify_prediction(risk_val)
        
    total_time = time.perf_counter() - start_time
    avg_latency_ms = (total_time / num_runs) * 1000
    print(f"Benchmark Complete: {num_runs} Z3 verification runs.")
    print(f"Average Latency: {avg_latency_ms:.4f} ms per verification check.")

if __name__ == "__main__":
    run_latency_benchmark()