from typing import Optional

from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy
from sqlalchemy.sql import select, or_

from db.schema import countries


API_MAX_LIMIT = 200


async def get_all_countries(conn: PoolConnectionProxy, *, limit: int = 0):
    """"""

    sql = select([countries])
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_countries = await conn.fetch(sql)

    return all_countries


async def get_countries_by_substring(
    conn: PoolConnectionProxy, *, substring: str, limit: int = 0
) -> Optional[Record]:
    """"""

    sql = select([countries]).where(
        or_(
            countries.c.name.ilike(f"%{substring}%"),
            countries.c.code.ilike(f"%{substring}%"),
        )
    )
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_countries = await conn.fetch(sql)

    return all_countries
