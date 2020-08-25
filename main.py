from aiohttp import web


async def index(request):
    return web.json_response({"result": "ok"})


app = web.Application()

app.router.add_get("/", index)

web.run_app(app)
