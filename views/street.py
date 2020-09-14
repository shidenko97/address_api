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
    """
    ---
    description: Get list of streets by district id.
    tags:
        - Streets
    produces:
        - application/json
    parameters:
        - in: path
          name: district_id
          description: District for street.
          type: int
          required: true
        - in: query
          name: q
          description: Substring to filter results.
          type: str
          requires: false
        - in: query
          name: limit
          description: Max count of streets in list. Maximum is 200.
          default: 200
          type: int
          requires: false
    responses:
        "200":
            description: List of streets.
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: "#/components/schemas/Street"
    """

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
    """
    ---
    description: Get list of streets by locality id.
    tags:
        - Streets
    produces:
        - application/json
    parameters:
        - in: path
          name: locality_id
          description: Locality for street.
          type: int
          required: true
        - in: query
          name: q
          description: Substring to filter results.
          type: str
          requires: false
        - in: query
          name: limit
          description: Max count of streets in list. Maximum is 200.
          default: 200
          type: int
          requires: false
    responses:
        "200":
            description: List of streets.
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: "#/components/schemas/Street"
    """

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
    """
    ---
    description: Get street by id.
    method: GET
    tags:
        - Streets
    produces:
        - application/json
    parameters:
        - in: path
          name: street_id
          description: Street id.
          type: int
          required: true
    responses:
        "200":
            description: Street object.
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/Street"
    """

    street_id = int(request.match_info.get("street_id"))

    async with request.app["db"].acquire() as conn:

        street_object = await get_street(conn, street_id=street_id)

    return web.json_response(text=to_json(street_object))
