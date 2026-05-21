import pytest
from core.symbolic_verifier import SymbolicGuardrail

def test_symbolic_verifier_pass():
    """Verify that predictions below or equal to threshold pass the Z3 solver."""
    verifier = SymbolicGuardrail(max_allowed_risk=0.75)
    passed, msg = verifier.verify_prediction(0.65)
    assert passed is True
    assert "SATISFIED" in msg

def test_symbolic_verifier_fail():
    """Verify that predictions exceeding the threshold fail the Z3 solver."""
    verifier = SymbolicGuardrail(max_allowed_risk=0.75)
    passed, msg = verifier.verify_prediction(0.82)
    assert passed is False
    assert "VIOLATION" in msg

def test_symbolic_verifier_boundary():
    """Verify exact boundary behavior."""
    verifier = SymbolicGuardrail(max_allowed_risk=0.75)
    passed, _ = verifier.verify_prediction(0.75)
    assert passed is True