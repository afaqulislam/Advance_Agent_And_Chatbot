# server.py
import os
from chainlit.server import app
from uvicorn import Config, Server
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware


# =============================================
# FORCE HTTPS MIDDLEWARE (SIMPLE & SAFE)
# =============================================
class ForceHTTPSMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # ONLY CHANGE SCHEME — NO HEADER TOUCHING
        request.scope["scheme"] = "https"
        return await call_next(request)


# Add middleware
app.add_middleware(ForceHTTPSMiddleware)

# =============================================
# RUN SERVER
# =============================================
if __name__ == "__main__":
    config = Config(
        app=app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        proxy_headers=True,
        forwarded_allow_ips=["*"],
    )
    server = Server(config)
    server.run()

