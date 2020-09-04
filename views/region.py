from aiohttp import web

from logic.api import (
    get_regions_in_country_by_substring,
    get_all_regions_in_country,
    get_region,
)
from utils.json_serializer import to_json


async def all_regions_in_country(request: web.Request):
    """Get all regions."""

    country_id = int(request.match_info.get("country_id", "0"))

    q = request.rel_url.query.get("q")
    limit = int(request.rel_url.query.get("limit", "0"))

    async with request.app["db"].acquire() as conn:

        if q:
            regions_objects = await get_regions_in_country_by_substring(
                conn, country_id=country_id, substring=q, limit=limit
            )
        else:
            regions_objects = await get_all_regions_in_country(
                conn, country_id=country_id, limit=limit
            )

    return web.json_response(text=to_json(regions_objects))


async def get_one_region(request: web.Request):
    """Get region by id."""

    region_id = int(request.match_info.get("region_id"))

    async with request.app["db"].acquire() as conn:

        region_object = await get_region(conn, region_id=region_id)

    return web.json_response(text=to_json(region_object))
