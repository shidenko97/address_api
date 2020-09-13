from aiohttp import web

from logic.api import (
    get_regions_in_country_by_substring,
    get_all_regions_in_country,
    get_region,
)
from utils.json_serializer import to_json


async def all_regions_in_country(request: web.Request):
    """
    ---
    description: Get list of regions by country id.
    tags:
        - Regions
    produces:
        - application/json
    parameters:
        - in: path
          name: country_id
          description: Country for region.
          type: int
          required: true
        - in: query
          name: q
          description: Substring to filter results.
          type: str
          requires: false
        - in: query
          name: limit
          description: Max count of regions in list. Maximum is 200.
          default: 200
          type: int
          requires: false
    responses:
        "200":
            description: List of regions.
    """

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
    """
    ---
    description: Get region by id.
    method: GET
    tags:
        - Regions
    produces:
        - application/json
    parameters:
        - in: path
          name: region_id
          description: Region id.
          type: int
          required: true
    responses:
        "200":
            description: Region object.
    """

    region_id = int(request.match_info.get("region_id"))

    async with request.app["db"].acquire() as conn:

        region_object = await get_region(conn, region_id=region_id)

    return web.json_response(text=to_json(region_object))
