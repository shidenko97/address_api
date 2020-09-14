from aiohttp import web

from logic.api import (
    get_localities_in_area_by_substring,
    get_all_localities_in_area,
    get_locality,
    get_localities_by_substring,
    get_all_localities,
)
from utils.json_serializer import to_json


async def all_localities(request: web.Request):
    """
    ---
    description: Get list of localities.
    tags:
        - Localities
    produces:
        - application/json
    parameters:
        - in: query
          name: q
          description: Substring to filter results.
          type: str
          requires: false
        - in: query
          name: limit
          description: Max count of localities in list. Maximum is 200.
          default: 200
          type: int
          requires: false
    responses:
        "200":
            description: List of localities.
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: "#/components/schemas/Locality"
    """

    q = request.rel_url.query.get("q")
    limit = int(request.rel_url.query.get("limit", "0"))

    async with request.app["db"].acquire() as conn:

        if q:
            localities_objects = await get_localities_by_substring(
                conn, substring=q, limit=limit
            )
        else:
            localities_objects = await get_all_localities(conn, limit=limit)

    return web.json_response(text=to_json(localities_objects))


async def all_localities_in_area(request: web.Request):
    """
    ---
    description: Get list of localities by area id.
    tags:
        - Localities
    produces:
        - application/json
    parameters:
        - in: path
          name: area_id
          description: Area for locality.
          type: int
          required: true
        - in: query
          name: q
          description: Substring to filter results.
          type: str
          requires: false
        - in: query
          name: limit
          description: Max count of localities in list. Maximum is 200.
          default: 200
          type: int
          requires: false
    responses:
        "200":
            description: List of localities.
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: "#/components/schemas/Locality"
    """

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
    """
    ---
    description: Get locality by id.
    method: GET
    tags:
        - Localities
    produces:
        - application/json
    parameters:
        - in: path
          name: locality_id
          description: Locality id.
          type: int
          required: true
    responses:
        "200":
            description: Locality object.
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/Locality"
    """

    locality_id = int(request.match_info.get("locality_id"))

    async with request.app["db"].acquire() as conn:

        locality_object = await get_locality(conn, locality_id=locality_id)

    return web.json_response(text=to_json(locality_object))
