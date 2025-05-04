from litestar import Litestar, get


@get("/ping")
async def ping() -> dict[str, str]:
    return {"ping": "pong"}

app = Litestar(route_handlers=[ping])
