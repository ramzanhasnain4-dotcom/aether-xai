from fastapi import FastAPI
from api.middleware import TenantContextMiddleware
from api.routes import router

app = FastAPI(
    title="Aether-XAI Engine",
    description="Multi-Tenant Neuro-Symbolic Verification Engine",
    version="1.0.0"
)

app.add_middleware(TenantContextMiddleware)
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "Aether-XAI"}