from aiohttp import web

from logic.api import (
    get_streets_in_district_by_substring,
    get_all_streets_in_district,
    get_streets_in_locality_by_substring,
    get_all_streets_in_locality,
    get_street,
)
from utils.json_serializer import to_json


async def all_streets_in_district(request: web.Request):
    """Get all districts."""

    district_id = int(request.match_info.get("district_id", "0"))

    q = request.rel_url.query.get("q")
    limit = int(request.rel_url.query.get("limit", "0"))

    async with request.app["db"].acquire() as conn:

        if q:
            streets_objects = await get_streets_in_district_by_substring(
                conn, district_id=district_id, substring=q, limit=limit
            )
        else:
            streets_objects = await get_all_streets_in_district(
                conn, district_id=district_id, limit=limit
            )

    return web.json_response(text=to_json(streets_objects))


async def all_streets_in_locality(request: web.Request):
    """Get all districts."""

    locality_id = int(request.match_info.get("locality_id", "0"))

    q = request.rel_url.query.get("q")
    limit = int(request.rel_url.query.get("limit", "0"))

    async with request.app["db"].acquire() as conn:

        if q:
            streets_objects = await get_streets_in_locality_by_substring(
                conn, locality_id=locality_id, substring=q, limit=limit
            )
        else:
            streets_objects = await get_all_streets_in_locality(
                conn, locality_id=locality_id, limit=limit
            )

    return web.json_response(text=to_json(streets_objects))


async def get_one_street(request: web.Request):
    """Get street by id."""

    street_id = int(request.match_info.get("street_id"))

    async with request.app["db"].acquire() as conn:

        street_object = await get_street(conn, street_id=street_id)

    return web.json_response(text=to_json(street_object))
