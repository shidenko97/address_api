from aiohttp import web

from logic.api import (
    get_districts_in_locality_by_substring,
    get_all_districts_in_locality,
    get_district,
)
from utils.json_serializer import to_json


async def all_districts_in_locality(request: web.Request):
    """
    ---
    description: Get list of districts by locality id.
    tags:
        - Districts
    produces:
        - application/json
    parameters:
        - in: path
          name: locality_id
          description: Locality for district.
          type: int
          required: true
        - in: query
          name: q
          description: Substring to filter results.
          type: str
          requires: false
        - in: query
          name: limit
          description: Max count of districts in list. Maximum is 200.
          default: 200
          type: int
          requires: false
    responses:
        "200":
            description: List of districts.
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: "#/components/schemas/District"
    """

    locality_id = int(request.match_info.get("locality_id", "0"))

    q = request.rel_url.query.get("q")
    limit = int(request.rel_url.query.get("limit", "0"))

    async with request.app["db"].acquire() as conn:

        if q:
            districts_objects = await get_districts_in_locality_by_substring(
                conn, locality_id=locality_id, substring=q, limit=limit
            )
        else:
            districts_objects = await get_all_districts_in_locality(
                conn, locality_id=locality_id, limit=limit
            )

    return web.json_response(text=to_json(districts_objects))


async def get_one_district(request: web.Request):
    """
    ---
    description: Get district by id.
    method: GET
    tags:
        - Districts
    produces:
        - application/json
    parameters:
        - in: path
          name: district_id
          description: District id.
          type: int
          required: true
    responses:
        "200":
            description: District object.
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/District"
    """

    district_id = int(request.match_info.get("district_id"))

    async with request.app["db"].acquire() as conn:

        district_object = await get_district(conn, district_id=district_id)

    return web.json_response(text=to_json(district_object))
