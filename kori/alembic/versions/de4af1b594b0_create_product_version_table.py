"""create product_version table

Revision ID: de4af1b594b0
Revises: 2f4cdef0f290
Create Date: 2023-02-12 20:21:40.268996

"""
import datetime
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = "de4af1b594b0"
down_revision = "2f4cdef0f290"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_version",
        sa.Column("product_id", UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column("version_id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("price", sa.Numeric(10, 3), nullable=False),
        sa.Column("measurement_unit", sa.String(16), nullable=False),
        sa.Column("valid_from", sa.types.TIMESTAMP, nullable=False),
        sa.Column("valid_to", sa.types.TIMESTAMP, nullable=True),
        sa.ForeignKeyConstraint(("product_id",), ["product.id"]),
    )


def downgrade() -> None:
    op.drop_table("product_version")
