from aiohttp import web

from logic.api import (
    get_localities_in_area_by_substring,
    get_all_localities_in_area,
    get_locality,
)
from utils.json_serializer import to_json


async def all_localities_in_area(request: web.Request):
    """Get all localities."""

    area_id = int(request.match_info.get("area_id", "0"))

    q = request.rel_url.query.get("q")
    limit = int(request.rel_url.query.get("limit", "0"))

    async with request.app["db"].acquire() as conn:

        if q:
            localities_objects = await get_localities_in_area_by_substring(
                conn, area_id=area_id, substring=q, limit=limit
            )
        else:
            localities_objects = await get_all_localities_in_area(
                conn, area_id=area_id, limit=limit
            )

    return web.json_response(text=to_json(localities_objects))


async def get_one_locality(request: web.Request):
    """Get locality by id."""

    locality_id = int(request.match_info.get("locality_id"))

    async with request.app["db"].acquire() as conn:

        locality_object = await get_locality(conn, locality_id=locality_id)

    return web.json_response(text=to_json(locality_object))
