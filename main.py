from aiohttp import web

from config import Config
from db import init_db
from views import country


def main() -> None:
    """Application entrypoint."""

    config = Config.load_config()

    app = init_app(config=config)

    web.run_app(app)


def setup_routes(*, app: web.Application) -> None:
    """
    Setup application routes.

    :param app: Current application
    :type app: web.Application
    """

    router = app.router

    router.add_get("/countries", country.all_countries)


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

    app["config"] = config
    app["db"] = await init_db(config=config)

    return app


if __name__ == "__main__":
    main()
