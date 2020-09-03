from aiohttp import web

from logic.api import get_all_countries, get_countries_by_substring
from utils.json_serializer import to_json


async def all_countries(request: web.Request):
    """Get all countries."""

    q = request.rel_url.query.get("q")
    limit = int(request.rel_url.query.get("limit", "0"))

    async with request.app["db"].acquire() as conn:

        if q:
            countries = await get_countries_by_substring(
                conn, substring=q, limit=limit
            )
        else:
            countries = await get_all_countries(conn, limit=limit)

    return web.json_response(text=to_json(countries))
