from typing import Optional, Union

from asyncpg import Record
from asyncpg.pool import PoolConnectionProxy
from sqlalchemy.sql import and_, or_, select

from db.schema import (
    areas,
    countries,
    districts,
    houses,
    localities,
    regions,
    streets,
)
from logic.entities import (
    Area,
    Country,
    District,
    House,
    Locality,
    Region,
    Street,
)


async def find_country(
    conn: PoolConnectionProxy, *, country: Country
) -> Optional[Record]:
    """
    Find country record in database by name or code and return it.
    If it doesn't exist - return None.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param country: Country object
    :type country: Country
    :return: Country record if found, otherwise None
    :rtype: Optional[Record]
    """

    country_obj = await conn.fetchrow(
        select([countries]).where(
            or_(
                countries.c.name == country.name,
                countries.c.code == country.code,
            )
        )
    )

    return country_obj


async def add_country(
    conn: PoolConnectionProxy, *, country: Country
) -> Union[int, bool]:
    """
    Add country record into database or return False if present.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param country: Country object
    :type country: Country
    :return: Added country record id or False if present
    :rtype: Union[int, False]
    """

    if (await find_country(conn, country=country)) is not None:
        return False

    country_id = await conn.fetchval(
        """
        INSERT INTO
            country (name, code)
        VALUES
            ($1, $2)
        RETURNING id
        """,
        country.name,
        country.code,
    )

    return country_id


async def find_region(
    conn: PoolConnectionProxy, *, region: Region
) -> Optional[Record]:
    """
    Find region record in database by name and country id and return it.
    If it doesn't exist - return None.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param region: Region object
    :type region: Region
    :return: Region record if found, otherwise None
    :rtype: Optional[Record]
    """

    region_obj = await conn.fetchrow(
        select([regions]).where(
            and_(
                regions.c.name == region.name,
                regions.c.country_id == region.country_id,
            )
        )
    )

    return region_obj


async def add_region(
    conn: PoolConnectionProxy, *, region: Region
) -> Union[int, bool]:
    """
    Add region record into database or return False if present.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param region: Region object
    :type region: Region
    :return: Added region record id or False if present
    :rtype: Union[int, False]
    """

    if (await find_region(conn, region=region)) is not None:
        return False

    region_id = await conn.fetchval(
        """
        INSERT INTO
            region (country_id, name, geoip_name)
        VALUES
            ($1, $2, $3)
        RETURNING id
        """,
        region.country_id,
        region.name,
        region.geoip_name,
    )

    return region_id


async def find_area(
    conn: PoolConnectionProxy, *, area: Area
) -> Optional[Record]:
    """
    Find area record in database by name and region id and return it.
    If it doesn't exist - return None.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param area: Area object
    :type area: Area
    :return: Area record if found, otherwise None
    :rtype: Optional[Record]
    """

    area_obj = await conn.fetchrow(
        select([areas]).where(
            and_(
                areas.c.name == area.name, areas.c.region_id == area.region_id
            )
        )
    )

    return area_obj


async def add_area(
    conn: PoolConnectionProxy, *, area: Area
) -> Union[int, bool]:
    """
    Add area record into database or return False if present.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param area: Area object
    :type area: Area
    :return: Added area record id or False if present
    :rtype: Union[int, False]
    """

    if (await find_area(conn, area=area)) is not None:
        return False

    area_id = await conn.fetchval(
        """
        INSERT INTO
            area (region_id, name)
        VALUES
            ($1, $2)
        RETURNING id
        """,
        area.region_id,
        area.name,
    )

    return area_id


async def find_locality(
    conn: PoolConnectionProxy, *, locality: Locality
) -> Optional[Record]:
    """
    Find locality record in database by name and area id and return it.
    If it doesn't exist - return None.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param locality: Locality object
    :type locality: Locality
    :return: Locality record if found, otherwise None
    :rtype: Optional[Record]
    """

    locality_obj = await conn.fetchrow(
        select([localities]).where(
            and_(
                localities.c.name == locality.name,
                localities.c.area_id == locality.area_id,
            )
        )
    )

    return locality_obj


async def add_locality(
    conn: PoolConnectionProxy, *, locality: Locality
) -> Union[int, bool]:
    """
    Add locality record into database or return False if present.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param locality: Locality object
    :type locality: Locality
    :return: Added locality record id or False if present
    :rtype: Union[int, False]
    """

    if (await find_locality(conn, locality=locality)) is not None:
        return False

    locality_id = await conn.fetchval(
        """
        INSERT INTO
            locality (area_id, name)
        VALUES
            ($1, $2)
        RETURNING id
        """,
        locality.area_id,
        locality.name,
    )

    return locality_id


async def find_district(
    conn: PoolConnectionProxy, *, district: District
) -> Optional[Record]:
    """
    Find district record in database by name and locality id and return it.
    If it doesn't exist - return None.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param district: District object
    :type district: District
    :return: District record if found, otherwise None
    :rtype: Optional[Record]
    """

    district_obj = await conn.fetchrow(
        select([districts]).where(
            and_(
                districts.c.name == district.name,
                districts.c.locality_id == district.locality_id,
            )
        )
    )

    return district_obj


async def add_district(
    conn: PoolConnectionProxy, *, district: District
) -> Union[int, bool]:
    """
    Add district record into database or return False if present.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param district: District object
    :type district: District
    :return: Added district record id or False if present
    :rtype: Union[int, False]
    """

    if (await find_district(conn, district=district)) is not None:
        return False

    district_id = await conn.fetchval(
        """
        INSERT INTO
            district (locality_id, name)
        VALUES
            ($1, $2)
        RETURNING id
        """,
        district.locality_id,
        district.name,
    )

    return district_id


async def find_street(
    conn: PoolConnectionProxy, *, street: Street
) -> Optional[Record]:
    """
    Find street record in database by name and district id and return it.
    If it doesn't exist - return None.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param street: Street object
    :type street: Street
    :return: Street record if found, otherwise None
    :rtype: Optional[Record]
    """

    street_obj = await conn.fetchrow(
        select([streets]).where(
            and_(
                streets.c.name == street.name,
                streets.c.district_id == street.district_id,
            )
        )
    )

    return street_obj


async def add_street(
    conn: PoolConnectionProxy, *, street: Street
) -> Union[int, bool]:
    """
    Add street record into database or return False if present.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param street: Street object
    :type street: Street
    :return: Added street record id or False if present
    :rtype: Union[int, False]
    """

    if (await find_street(conn, street=street)) is not None:
        return False

    street_id = await conn.fetchval(
        """
        INSERT INTO
            street (district_id, name)
        VALUES
            ($1, $2)
        RETURNING id
        """,
        street.district_id,
        street.name,
    )

    return street_id


async def find_house(
    conn: PoolConnectionProxy, *, house: House
) -> Optional[Record]:
    """
    Find house record in database by number and street id and return it.
    If it doesn't exist - return None.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param house: House object
    :type house: House
    :return: House record if found, otherwise None
    :rtype: Optional[Record]
    """

    house_obj = await conn.fetchrow(
        select([houses]).where(
            and_(
                houses.c.number == house.number,
                houses.c.street_id == house.street_id,
            )
        )
    )

    return house_obj


async def add_house(
    conn: PoolConnectionProxy, *, house: House
) -> Union[int, bool]:
    """
    Add house record into database or return False if present.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param house: House object
    :type house: House
    :return: Added house record id or False if present
    :rtype: Union[int, False]
    """

    if (await find_house(conn, house=house)) is not None:
        return False

    house_id = await conn.fetchval(
        """
        INSERT INTO
            house (street_id, number, index)
        VALUES
            ($1, $2, $3)
        RETURNING id
        """,
        house.street_id,
        house.number,
        house.index,
    )

    return house_id
