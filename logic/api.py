from typing import Optional

from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy
from sqlalchemy.sql import select, or_, and_

from db.schema import (
    countries,
    regions,
    areas,
    localities,
    districts,
    streets,
    houses,
)


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


async def get_country(conn: PoolConnectionProxy, *, country_id: int):
    """"""

    country = await conn.fetchrow(
        select([countries]).where(countries.c.id == country_id)
    )

    return country


async def get_regions_in_country_by_substring(
    conn: PoolConnectionProxy,
    *,
    country_id: int,
    substring: str,
    limit: int = 0,
):
    """"""

    sql = select([regions]).where(
        and_(
            regions.c.country_id == country_id,
            regions.c.name.ilike(f"%{substring}%"),
        )
    )
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_regions = await conn.fetch(sql)

    return all_regions


async def get_all_regions_in_country(
    conn: PoolConnectionProxy, *, country_id: int, limit: int = 0
):
    """"""

    sql = select([regions]).where(regions.c.country_id == country_id)
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_regions = await conn.fetch(sql)

    return all_regions


async def get_region(conn: PoolConnectionProxy, *, region_id: int):
    """"""

    region = await conn.fetchrow(
        select([regions]).where(regions.c.id == region_id)
    )

    return region


async def get_areas_in_region_by_substring(
    conn: PoolConnectionProxy,
    *,
    region_id: int,
    substring: str,
    limit: int = 0,
):
    """"""

    sql = select([areas]).where(
        and_(
            areas.c.region_id == region_id,
            areas.c.name.ilike(f"%{substring}%"),
        )
    )
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_areas = await conn.fetch(sql)

    return all_areas


async def get_all_areas_in_region(
    conn: PoolConnectionProxy, *, region_id: int, limit: int = 0
):
    """"""

    sql = select([areas]).where(areas.c.region_id == region_id)
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_areas = await conn.fetch(sql)

    return all_areas


async def get_area(conn: PoolConnectionProxy, *, area_id: int):
    """"""

    area = await conn.fetchrow(select([areas]).where(areas.c.id == area_id))

    return area


async def get_localities_in_area_by_substring(
    conn: PoolConnectionProxy, *, area_id: int, substring: str, limit: int = 0
):
    """"""

    sql = select([localities]).where(
        and_(
            localities.c.area_id == area_id,
            localities.c.name.ilike(f"%{substring}%"),
        )
    )
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_localities = await conn.fetch(sql)

    return all_localities


async def get_all_localities_in_area(
    conn: PoolConnectionProxy, *, area_id: int, limit: int = 0
):
    """"""

    sql = select([localities]).where(localities.c.area_id == area_id)
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_localities = await conn.fetch(sql)

    return all_localities


async def get_locality(conn: PoolConnectionProxy, *, locality_id: int):
    """"""

    locality = await conn.fetchrow(
        select([localities]).where(localities.c.id == locality_id)
    )

    return locality


async def get_districts_in_locality_by_substring(
    conn: PoolConnectionProxy,
    *,
    locality_id: int,
    substring: str,
    limit: int = 0,
):
    """"""

    sql = select([districts]).where(
        and_(
            districts.c.locality_id == locality_id,
            districts.c.name.ilike(f"%{substring}%"),
        )
    )
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_districts = await conn.fetch(sql)

    return all_districts


async def get_all_districts_in_locality(
    conn: PoolConnectionProxy, *, locality_id: int, limit: int = 0
):
    """"""

    sql = select([districts]).where(districts.c.locality_id == locality_id)
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_districts = await conn.fetch(sql)

    return all_districts


async def get_district(conn: PoolConnectionProxy, *, district_id: int):
    """"""

    district = await conn.fetchrow(
        select([districts]).where(districts.c.id == district_id)
    )

    return district


async def get_streets_in_district_by_substring(
    conn: PoolConnectionProxy,
    *,
    district_id: int,
    substring: str,
    limit: int = 0,
):
    """"""

    sql = select([streets]).where(
        and_(
            streets.c.district_id == district_id,
            streets.c.name.ilike(f"%{substring}%"),
        )
    )
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_streets = await conn.fetch(sql)

    return all_streets


async def get_all_streets_in_district(
    conn: PoolConnectionProxy, *, district_id: int, limit: int = 0
):
    """"""

    sql = select([streets]).where(streets.c.district_id == district_id)
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_streets = await conn.fetch(sql)

    return all_streets


async def get_streets_in_locality_by_substring(
    conn: PoolConnectionProxy,
    *,
    locality_id: int,
    substring: str,
    limit: int = 0,
):
    """"""

    join = streets.join(districts, streets.c.district_id == districts.c.id)
    sql = (
        select([streets])
        .select_from(join)
        .where(
            and_(
                districts.c.locality_id == locality_id,
                streets.c.name.ilike(f"%{substring}%"),
            )
        )
    )
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_streets = await conn.fetch(sql)

    return all_streets


async def get_all_streets_in_locality(
    conn: PoolConnectionProxy, *, locality_id: int, limit: int = 0
):
    """"""

    join = streets.join(districts, streets.c.district_id == districts.c.id)
    sql = (
        select([streets])
        .select_from(join)
        .where(districts.c.locality_id == locality_id)
    )
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_streets = await conn.fetch(sql)

    return all_streets


async def get_street(conn: PoolConnectionProxy, *, street_id: int):
    """"""

    street = await conn.fetchrow(
        select([streets]).where(streets.c.id == street_id)
    )

    return street


async def get_houses_in_street_by_substring(
    conn: PoolConnectionProxy,
    *,
    street_id: int,
    substring: str,
    limit: int = 0,
):
    """"""

    sql = select([houses]).where(
        and_(
            houses.c.street_id == street_id,
            houses.c.number.ilike(f"%{substring}%"),
        )
    )
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_houses = await conn.fetch(sql)

    return all_houses


async def get_all_houses_in_street(
    conn: PoolConnectionProxy, *, street_id: int, limit: int = 0
):
    """"""

    sql = select([houses]).where(houses.c.street_id == street_id)
    limit = max(0, min(limit, API_MAX_LIMIT))

    if limit:
        sql = sql.limit(limit)

    all_houses = await conn.fetch(sql)

    return all_houses


async def get_house(conn: PoolConnectionProxy, *, house_id: int):
    """"""

    house = await conn.fetchrow(
        select([houses]).where(houses.c.id == house_id)
    )

    return house


async def get_full_address_by_house(
    conn: PoolConnectionProxy, *, house_id: int
):
    """"""

    join = (
        houses.join(streets, houses.c.street_id == streets.c.id)
        .join(districts, streets.c.district_id == districts.c.id)
        .join(localities, districts.c.locality_id == localities.c.id)
        .join(areas, localities.c.area_id == areas.c.id)
        .join(regions, areas.c.region_id == regions.c.id)
        .join(countries, regions.c.country_id == countries.c.id)
    )
    sql = (
        select(
            [
                countries.c.name.label("country"),
                regions.c.name.label("region"),
                areas.c.name.label("area"),
                localities.c.name.label("locality"),
                districts.c.name.label("district"),
                streets.c.name.label("street"),
                houses.c.number.label("house"),
                houses.c.index.label("index"),
            ]
        )
        .select_from(join)
        .where(houses.c.id == house_id)
    )

    full_address = await conn.fetchrow(sql)

    return full_address
