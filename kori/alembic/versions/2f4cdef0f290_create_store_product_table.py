"""create store_product table

Revision ID: 2f4cdef0f290
Revises: 523744512cc0
Create Date: 2023-02-12 20:16:50.651291

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = "2f4cdef0f290"
down_revision = "523744512cc0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "store_product",
        sa.Column("product_id", UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column("store_id", UUID(as_uuid=True), nullable=False, primary_key=True),
        sa.Column("stock_available", sa.Integer(), nullable=False),
        sa.Column("stock_locked", sa.Integer(), nullable=False, default=0),
        sa.ForeignKeyConstraint(("product_id",), ["product.id"]),
        sa.ForeignKeyConstraint(("store_id",), ["store.id"]),
    )


def downgrade() -> None:
    op.drop_table("store_product")
