from z3 import Solver, Real, sat

class SymbolicGuardrail:
    """Uses Z3 SMT Solver to formally verify if neural network outputs satisfy tenant safety rules."""

    def __init__(self, max_allowed_risk: float):
        # Round threshold to prevent floating-point representation drift in Z3
        self.max_allowed_risk = round(float(max_allowed_risk), 4)

    def verify_prediction(self, predicted_risk: float) -> tuple[bool, str]:
        s = Solver()
        risk = Real('risk')
        
        # Round input risk float to match precision
        clean_risk = round(float(predicted_risk), 4)
        
        # Formulate formal logical propositions
        s.add(risk == clean_risk)
        s.add(risk <= self.max_allowed_risk)
        
        if s.check() == sat:
            return True, f"SATISFIED: Risk {clean_risk:.4f} <= threshold {self.max_allowed_risk:.4f}"
        else:
            return False, f"VIOLATION: Risk {clean_risk:.4f} exceeds max threshold {self.max_allowed_risk:.4f}"