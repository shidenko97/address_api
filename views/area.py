from aiohttp import web

from logic.api import (
    get_areas_in_region_by_substring,
    get_all_areas_in_region,
    get_area,
)
from utils.json_serializer import to_json


async def all_areas_in_region(request: web.Request):
    """Get all areas."""

    region_id = int(request.match_info.get("region_id", "0"))

    q = request.rel_url.query.get("q")
    limit = int(request.rel_url.query.get("limit", "0"))

    async with request.app["db"].acquire() as conn:

        if q:
            areas_objects = await get_areas_in_region_by_substring(
                conn, region_id=region_id, substring=q, limit=limit
            )
        else:
            areas_objects = await get_all_areas_in_region(
                conn, region_id=region_id, limit=limit
            )

    return web.json_response(text=to_json(areas_objects))


async def get_one_area(request: web.Request):
    """Get area by id."""

    area_id = int(request.match_info.get("area_id"))

    async with request.app["db"].acquire() as conn:

        area_object = await get_area(conn, area_id=area_id)

    return web.json_response(text=to_json(area_object))
