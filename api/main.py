from fastapi import FastAPI

app = FastAPI(
    title="Aether-XAI Engine",
    description="Multi-Tenant Neuro-Symbolic Verification Engine",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "engine": "Aether-XAI"}