from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException

class TenantContextMiddleware(BaseHTTPMiddleware):
    """Extracts X-Tenant-ID header and injects tenant context into request state."""
    
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/api/v1"):
            tenant_id = request.headers.get("X-Tenant-ID")
            if not tenant_id:
                raise HTTPException(status_code=400, detail="Missing X-Tenant-ID header.")
            request.state.tenant_id = tenant_id
            
        response = await call_next(request)
        return response
    