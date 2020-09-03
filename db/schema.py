from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table
from sqlalchemy.dialects.postgresql import ENUM

from db import NAMING_CONVECTION


metadata = MetaData(naming_convention=NAMING_CONVECTION)

countries = Table(
    "country",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(64), nullable=False),
    Column("code", String(2), nullable=False, unique=True),
)

regions = Table(
    "region",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "country_id",
        Integer,
        ForeignKey("country.id"),
        nullable=False,
        index=True,
    ),
    Column("name", String(128), nullable=False),
    Column("geoip_name", String(128), nullable=False),
)

areas = Table(
    "area",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "region_id",
        Integer,
        ForeignKey("region.id"),
        nullable=False,
        index=True,
    ),
    Column("name", String(128), nullable=False),
)

localities = Table(
    "locality",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "area_id", Integer, ForeignKey("area.id"), nullable=False, index=True
    ),
    Column("name", String(128), nullable=False),
)

districts = Table(
    "district",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "locality_id",
        Integer,
        ForeignKey("locality.id"),
        nullable=False,
        index=True,
    ),
    Column("name", String(128), nullable=False),
)

streets = Table(
    "street",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "district_id",
        Integer,
        ForeignKey("district.id"),
        nullable=False,
        index=True,
    ),
    Column("name", String(128), nullable=False),
)

houses = Table(
    "house",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "street_id",
        Integer,
        ForeignKey("street.id"),
        nullable=False,
        index=True,
    ),
    Column("index", String(8), nullable=False, index=True),
    Column("number", String(32), nullable=False),
)

alternative_names = Table(
    "alternative_name",
    metadata,
    Column("id", Integer, primary_key=True),
    Column(
        "type",
        ENUM(
            "country",
            "region",
            "area",
            "locality",
            "district",
            "street",
            "house",
            name="address_type_enum",
        ),
        nullable=False,
        index=True,
    ),
    Column("related_id", Integer, nullable=False, index=True),
)
