from aiohttp import web

from logic.api import (
    get_houses_in_street_by_substring,
    get_all_houses_in_street,
    get_house,
    get_full_address_by_house,
)
from utils.json_serializer import to_json


async def all_houses_in_street(request: web.Request):
    """
    ---
    description: Get list of areas by street id.
    tags:
        - Houses
    produces:
        - application/json
    parameters:
        - in: path
          name: street_id
          description: Street for house.
          type: int
          required: true
        - in: query
          name: q
          description: Substring to filter results.
          type: str
          requires: false
        - in: query
          name: limit
          description: Max count of houses in list. Maximum is 200.
          default: 200
          type: int
          requires: false
    responses:
        "200":
            description: List of houses.
            content:
                application/json:
                    schema:
                        type: array
                        items:
                            $ref: "#/components/schemas/House"
    """

    street_id = int(request.match_info.get("street_id", "0"))

    q = request.rel_url.query.get("q")
    limit = int(request.rel_url.query.get("limit", "0"))

    async with request.app["db"].acquire() as conn:

        if q:
            streets_objects = await get_houses_in_street_by_substring(
                conn, street_id=street_id, substring=q, limit=limit
            )
        else:
            streets_objects = await get_all_houses_in_street(
                conn, street_id=street_id, limit=limit
            )

    return web.json_response(text=to_json(streets_objects))


async def get_one_house(request: web.Request):
    """
    ---
    description: Get house by id.
    method: GET
    tags:
        - Houses
    produces:
        - application/json
    parameters:
        - in: path
          name: house_id
          description: House id.
          type: int
          required: true
    responses:
        "200":
            description: House object.
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/House"
    """

    house_id = int(request.match_info.get("house_id"))

    async with request.app["db"].acquire() as conn:

        house_object = await get_house(conn, house_id=house_id)

    return web.json_response(text=to_json(house_object))


async def get_full_address_by_one_house(request: web.Request):
    """
    ---
    description: Get full address by house.
    method: GET
    tags:
        - Houses
    produces:
        - application/json
    parameters:
        - in: path
          name: house_id
          description: House id.
          type: int
          required: true
    responses:
        "200":
            description: Full address object by house.
            content:
                application/json:
                    schema:
                        $ref: "#/components/schemas/FullAddress"
    """

    house_id = int(request.match_info.get("house_id"))

    async with request.app["db"].acquire() as conn:

        full_address = await get_full_address_by_house(conn, house_id=house_id)

    return web.json_response(text=to_json(full_address))
