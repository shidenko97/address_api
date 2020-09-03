import argparse
import asyncio
from typing import Union

from asyncpg.pool import PoolConnectionProxy

from config import Config
from db import init_db
from logic import upload as upload_module
from logic.entities import (
    Area,
    Country,
    District,
    House,
    Locality,
    Region,
    Street,
)
from source.base_source import BaseSource
from source.ukrposhta import Ukrposhta


SOURCES = {
    "Ukrposhta": Ukrposhta,
}


def _class_factory(*, source_name: str) -> BaseSource:
    """
    Get source class instance by class name.

    :param source_name: Class name
    :type source_name: str
    :return: Source class instance
    :rtype: BaseSource
    """

    source_class = SOURCES.get(source_name)
    return source_class()


async def _add_or_find_record(
    *,
    conn: PoolConnectionProxy,
    address_type: str,
    obj: Union[Country, Region, Area, Locality, District, Street, House],
    obj_attrs: dict,
) -> int:
    """
    Add new address record and return id of it.
    If record already exists - return id of it.

    :param conn: Pool of connections to database
    :type conn: PoolConnectionProxy
    :param address_type: Type of address record
    :type address_type: str
    :param obj: Object to add/find
    :type obj: Union[Country, Region, Area, Locality, District, Street, House]
    :param obj_attrs: Additional attributes for object
    :type obj_attrs: dict
    :raise: ValueError - can't find and add address record
    :return: Identifier of address record
    :rtype: int
    """

    print(f"{obj}", end=" - ")

    for attribute_name, attribute_value in obj_attrs.items():
        if hasattr(obj, attribute_name):
            setattr(obj, attribute_name, attribute_value)

    func_param_dict = {address_type: obj}

    find_function = getattr(upload_module, f"find_{address_type}")
    add_function = getattr(upload_module, f"add_{address_type}")

    if (
        existed_obj := await find_function(conn, **func_param_dict)
    ) is not None:
        object_id = existed_obj.get("id")
        print("exists", end=" ")
    elif object_id := await add_function(conn, **func_param_dict):
        print("created", end=" ")
    else:
        raise ValueError(f"Can't find/add {address_type} {obj}")
    print(f"[{object_id}]")

    return object_id


async def main(source_name: str):
    source = _class_factory(source_name=source_name)

    config = Config.load_config()
    db_pool = await init_db(config=config)

    async with db_pool.acquire() as conn:

        for row in source.get_address_rows():

            print(row)

            parent_name: str = ""
            parent_id: int = 0

            for address_type in (
                "Country",
                "Region",
                "Area",
                "Locality",
                "District",
                "Street",
                "House",
            ):
                lowed_type = address_type.lower()
                parent_id = await _add_or_find_record(
                    conn=conn,
                    address_type=lowed_type,
                    obj=row.get(address_type),
                    obj_attrs={parent_name: parent_id},
                )
                parent_name = f"{lowed_type}_id"


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-S",
        "--source",
        help="Source to upload addresses",
        required=True,
        choices=SOURCES.keys(),
    )

    args = parser.parse_args()
    task = loop.create_task(main(source_name=args.source))
    value = loop.run_until_complete(asyncio.wait([task]))

    loop.close()
