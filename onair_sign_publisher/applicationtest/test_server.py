""""
Copyright (C) 2021 twyleg
"""
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
