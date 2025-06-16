from litestar import Router, get

from app.api.accounts.controllers import AccessController, UserController


@get("/ping", tags=["healthcheck"])
async def ping() -> dict[str, str]:
    return {"ping": "pong"}


api_routers = Router(path="/", route_handlers=[ping, AccessController, UserController])
