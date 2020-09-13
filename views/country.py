from aiohttp import web

from logic.api import (
    get_all_countries,
    get_countries_by_substring,
    get_country,
)
from utils.json_serializer import to_json


async def all_countries(request: web.Request):
    """
    ---
    description: Get list of countries.
    tags:
        - Countries
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
          description: Max count of countries in list. Maximum is 200.
          default: 200
          type: int
          requires: false
    responses:
        "200":
            description: List of countries.
    """

    q = request.match_info.get("q")
    limit = int(request.match_info.get("limit", "0"))

    async with request.app["db"].acquire() as conn:

        if q:
            countries_objects = await get_countries_by_substring(
                conn, substring=q, limit=limit
            )
        else:
            countries_objects = await get_all_countries(conn, limit=limit)

    return web.json_response(text=to_json(countries_objects))


async def get_one_country(request: web.Request):
    """
    ---
    description: Get country by id.
    method: GET
    tags:
        - Countries
    produces:
        - application/json
    parameters:
        - in: path
          name: country_id
          description: Country id.
          type: int
          required: true
    responses:
        "200":
            description: Country object.
    """

    country_id = int(request.match_info.get("country_id"))

    async with request.app["db"].acquire() as conn:

        country_object = await get_country(conn, country_id=country_id)

    return web.json_response(text=to_json(country_object))
