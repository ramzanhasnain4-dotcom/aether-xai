from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel, Field
import torch
from core.neural_model import load_pretrained_model
from core.symbolic_verifier import SymbolicGuardrail
from core.explainability import XAIEngine

router = APIRouter(prefix="/api/v1")

model = load_pretrained_model()
xai = XAIEngine(feature_names=["f1", "f2", "f3", "f4", "f5"])

class InferenceRequest(BaseModel):
    features: list[float] = Field(..., min_length=5, max_length=5)
    max_risk_threshold: float = Field(default=0.70, ge=0.0, le=1.0)

class InferenceResponse(BaseModel):
    tenant_id: str
    raw_prediction: float
    constraint_passed: bool
    status_message: str
    attributions: dict[str, float]

@router.post("/predict", response_model=InferenceResponse)
async def predict_and_verify(payload: InferenceRequest, request: Request):
    tenant_id = getattr(request.state, "tenant_id", "anonymous")
    
    # 1. Neural Prediction
    inputs = torch.tensor([payload.features], dtype=torch.float32)
    with torch.no_grad():
        raw_pred = float(model(inputs).squeeze().item())
    
    # 2. Symbolic Formal Verification (Z3)
    verifier = SymbolicGuardrail(max_allowed_risk=payload.max_risk_threshold)
    passed, msg = verifier.verify_prediction(raw_pred)
    
    # 3. Explainability Attribution
    attributions = xai.compute_attributions(payload.features)
    
    return InferenceResponse(
        tenant_id=tenant_id,
        raw_prediction=round(raw_pred, 4),
        constraint_passed=passed,
        status_message=msg,
        attributions=attributions
    )