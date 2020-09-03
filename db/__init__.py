from typing import Any

import asyncpgsa
from asyncpg.pool import Pool
from sqlalchemy import create_engine


NAMING_CONVECTION = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
    "pk": "pk__%(table_name)s",
}


async def init_db(*, config: dict) -> Pool:
    """
    Initiate db connection.

    :param config: Application configuration
    :type config: dict
    :raise: ValueError - wrong db connection url
    :return: Pool of db connection
    :rtype: Pool
    """

    db_url = config["db_url"]

    if db_url.startswith("postgresql"):
        return await asyncpgsa.create_pool(dsn=db_url)

    raise ValueError("Wrong db connection")


def get_engine(*, config: dict) -> Any:
    """
    Get SQLAlchemy database engine.

    :param config: Application configuration
    :type config: dict
    :return: Database engine
    :rtype: Any
    """

    db_url = config["db_url"]

    return create_engine(db_url, isolation_level="AUTOCOMMIT")
