import chainlit as cl
from chainlit.server import app

# Run with proxy trust
if __name__ == "__main__":
    from uvicorn import Config, Server

    config = Config(
        app=app,
        host="0.0.0.0",
        port=int(cl.os.environ.get("PORT", 8080)),
        proxy_headers=True,  # This is key
        forwarded_allow_ips=["*"],  # Trust all (or specify Railway IPs)
    )
    server = Server(config)
    server.run()
