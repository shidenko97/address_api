from aiohttp import web
from aiohttp_swagger import setup_swagger

from config import Config
from db import init_db
from views import country, region, area, locality, district, street, house


def main() -> None:
    """Application entrypoint."""

    config = Config.load_config()

    app = init_app(config=config)

    web.run_app(app)


async def get_async_application() -> web.Application:
    """Application entrypoint."""

    config = Config.load_config()

    app = await init_app(config=config)

    return app


def setup_routes(*, app: web.Application) -> None:
    """
    Setup application routes.

    :param app: Current application
    :type app: web.Application
    """

    router = app.router

    router.add_get(
        "/country/{country_id:\\d+}", country.get_one_country, allow_head=False
    )
    router.add_get("/countries", country.all_countries, allow_head=False)

    router.add_get(
        "/region/{region_id:\\d+}", region.get_one_region, allow_head=False
    )
    router.add_get(
        "/regions/country-{country_id:\\d+}",
        region.all_regions_in_country,
        allow_head=False
    )

    router.add_get("/area/{area_id:\\d+}", area.get_one_area, allow_head=False)
    router.add_get(
        "/areas/region-{region_id:\\d+}",
        area.all_areas_in_region,
        allow_head=False
    )

    router.add_get(
        "/locality/{locality_id:\\d+}",
        locality.get_one_locality,
        allow_head=False
    )
    router.add_get(
        "/localities/area-{area_id:\\d+}",
        locality.all_localities_in_area,
        allow_head=False
    )

    router.add_get(
        "/district/{district_id:\\d+}",
        district.get_one_district,
        allow_head=False
    )
    router.add_get(
        "/districts/locality-{locality_id:\\d+}",
        district.all_districts_in_locality,
        allow_head=False
    )

    router.add_get(
        "/street/{street_id:\\d+}", street.get_one_street, allow_head=False
    )
    router.add_get(
        "/streets/locality-{locality_id:\\d+}",
        street.all_streets_in_locality,
        allow_head=False
    )
    router.add_get(
        "/streets/district-{district_id:\\d+}",
        street.all_streets_in_district,
        allow_head=False
    )

    router.add_get(
        "/house/{house_id:\\d+}", house.get_one_house, allow_head=False
    )
    router.add_get(
        "/house/{house_id:\\d+}/full",
        house.get_full_address_by_one_house,
        allow_head=False
    )
    router.add_get(
        "/houses/street-{street_id:\\d+}",
        house.all_houses_in_street,
        allow_head=False
    )


async def init_app(*, config: dict) -> web.Application:
    """
    Initialize instance of current application.

    :param config: Configuration for application
    :type config: dict
    :return: Current application
    :rtype: web.Application
    """

    app = web.Application()

    setup_routes(app=app)

    setup_swagger(
        app=app,
        swagger_url="/documentation",
        ui_version=3,
        description=(
            "Just a free address API. " +
            "You can upload your own data and use it for you web-forms. " +
            "In future you will can add streets and homes through the API."),
        title="Address API Documentation",
        api_version="1.0.0"
    )

    app["config"] = config
    app["db"] = await init_db(config=config)

    return app


if __name__ == "__main__":
    main()
