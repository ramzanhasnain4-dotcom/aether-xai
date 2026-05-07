from z3 import Solver, Real, sat

class SymbolicGuardrail:
    """Uses Z3 SMT Solver to formally verify if neural network outputs satisfy tenant safety rules."""

    def __init__(self, max_allowed_risk: float):
        self.max_allowed_risk = round(float(max_allowed_risk), 4)

    def verify_prediction(self, predicted_risk: float) -> tuple[bool, str]:
        s = Solver()
        risk = Real('risk')
        
        # Formulate formal logical propositions
        s.add(risk == float(predicted_risk))
        s.add(risk <= float(self.max_allowed_risk))
        
        if s.check() == sat:
            return True, f"SATISFIED: Risk {predicted_risk:.4f} <= threshold {self.max_allowed_risk:.4f}"
        else:
            return False, f"VIOLATION: Risk {predicted_risk:.4f} exceeds max threshold {self.max_allowed_risk:.4f}"