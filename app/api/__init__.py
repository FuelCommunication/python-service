from litestar import Router, get

from .accounts.controllers import AccessController, UserController
from .accounts.guards import auth
from .channels.controller import ChannelController


@get("/ping", tags=["healthcheck"])
async def ping() -> dict[str, str]:
    return {"ping": "pong"}


api_routers = Router(path="/", route_handlers=[ping, AccessController, UserController, ChannelController])
__all__ = (api_routers, auth)
