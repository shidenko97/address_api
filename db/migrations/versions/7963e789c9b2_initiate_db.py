"""Initiate db

Revision ID: 7963e789c9b2
Revises:
Create Date: 2020-09-03 10:21:24.664666

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "7963e789c9b2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "alternative_name",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "type",
            postgresql.ENUM(
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
        ),
        sa.Column("related_id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__alternative_name")),
    )
    op.create_index(
        op.f("ix__alternative_name__related_id"),
        "alternative_name",
        ["related_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix__alternative_name__type"),
        "alternative_name",
        ["type"],
        unique=False,
    )
    op.create_table(
        "country",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("code", sa.String(length=2), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__country")),
        sa.UniqueConstraint("code", name=op.f("uq__country__code")),
    )
    op.create_table(
        "region",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("country_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.Column("geoip_name", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["country_id"],
            ["country.id"],
            name=op.f("fk__region__country_id__country"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__region")),
    )
    op.create_index(
        op.f("ix__region__country_id"), "region", ["country_id"], unique=False
    )
    op.create_table(
        "area",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("region_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["region_id"],
            ["region.id"],
            name=op.f("fk__area__region_id__region"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__area")),
    )
    op.create_index(
        op.f("ix__area__region_id"), "area", ["region_id"], unique=False
    )
    op.create_table(
        "locality",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("area_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["area_id"], ["area.id"], name=op.f("fk__locality__area_id__area")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__locality")),
    )
    op.create_index(
        op.f("ix__locality__area_id"), "locality", ["area_id"], unique=False
    )
    op.create_table(
        "district",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("locality_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["locality_id"],
            ["locality.id"],
            name=op.f("fk__district__locality_id__locality"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__district")),
    )
    op.create_index(
        op.f("ix__district__locality_id"),
        "district",
        ["locality_id"],
        unique=False,
    )
    op.create_table(
        "street",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("district_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(
            ["district_id"],
            ["district.id"],
            name=op.f("fk__street__district_id__district"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__street")),
    )
    op.create_index(
        op.f("ix__street__district_id"),
        "street",
        ["district_id"],
        unique=False,
    )
    op.create_table(
        "house",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("street_id", sa.Integer(), nullable=False),
        sa.Column("index", sa.String(length=8), nullable=False),
        sa.Column("number", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(
            ["street_id"],
            ["street.id"],
            name=op.f("fk__house__street_id__street"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__house")),
    )
    op.create_index(op.f("ix__house__index"), "house", ["index"], unique=False)
    op.create_index(
        op.f("ix__house__street_id"), "house", ["street_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix__house__street_id"), table_name="house")
    op.drop_index(op.f("ix__house__index"), table_name="house")
    op.drop_table("house")
    op.drop_index(op.f("ix__street__district_id"), table_name="street")
    op.drop_table("street")
    op.drop_index(op.f("ix__district__locality_id"), table_name="district")
    op.drop_table("district")
    op.drop_index(op.f("ix__locality__area_id"), table_name="locality")
    op.drop_table("locality")
    op.drop_index(op.f("ix__area__region_id"), table_name="area")
    op.drop_table("area")
    op.drop_index(op.f("ix__region__country_id"), table_name="region")
    op.drop_table("region")
    op.drop_table("country")
    op.drop_index(
        op.f("ix__alternative_name__type"), table_name="alternative_name"
    )
    op.drop_index(
        op.f("ix__alternative_name__related_id"), table_name="alternative_name"
    )
    op.drop_table("alternative_name")
    # ### end Alembic commands ###
