import asyncio
from aiohttp import web, web_response, web_request

from aiohttp import web


async def handle(request):
    print(request.query)
    return web.Response(status=200)


app = web.Application()
app.add_routes([
    web.get('/onair', handle)
])

if __name__ == '__main__':
    web.run_app(app)

# async def handler(self, request: web_request.BaseRequest) -> web_response.Response:
#     print(request)
#     return web.Response(status=200)
#
#
# if __name__ == "__main__":
#     app = web.Application()
#     app.router.add_get('/onair_sign', handler)
#
#     runner = web.AppRunner(app)
#     asyncio.get_event_loop().run_until_complete(runner.setup())
#     site = web.TCPSite(runner, 'localhost', 8080)
#     asyncio.get_event_loop().run_until_complete(site.start())
