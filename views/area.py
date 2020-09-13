from aiohttp import web

from logic.api import (
    get_areas_in_region_by_substring,
    get_all_areas_in_region,
    get_area,
)
from utils.json_serializer import to_json


async def all_areas_in_region(request: web.Request):
    """
    ---
    description: Get list of areas by region id.
    tags:
        - Areas
    produces:
        - application/json
    parameters:
        - in: path
          name: region_id
          description: Region for area.
          type: int
          required: true
        - in: query
          name: q
          description: Substring to filter results.
          type: str
          requires: false
        - in: query
          name: limit
          description: Max count of areas in list. Maximum is 200.
          default: 200
          type: int
          requires: false
    responses:
        "200":
            description: List of areas.
    """

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
    """
    ---
    description: Get area by id.
    method: GET
    tags:
        - Areas
    produces:
        - application/json
    parameters:
        - in: path
          name: area_id
          description: Area id.
          type: int
          required: true
    responses:
        "200":
            description: Area object.
    """

    area_id = int(request.match_info.get("area_id"))

    async with request.app["db"].acquire() as conn:

        area_object = await get_area(conn, area_id=area_id)

    return web.json_response(text=to_json(area_object))
