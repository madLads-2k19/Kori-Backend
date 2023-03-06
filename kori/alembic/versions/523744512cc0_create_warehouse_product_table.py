"""create warehouse_product table

Revision ID: 523744512cc0
Revises: c48eb23a40bc
Create Date: 2023-02-12 20:12:20.324318

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = '523744512cc0'
down_revision = 'c48eb23a40bc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "warehouse_product",
        sa.Column("product_id", UUID(as_uuid=True), nullable=False),
        sa.Column("warehouse_id", UUID(as_uuid=True), nullable=False),
        sa.Column("stock_available", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(("product_id",), ["product.id"]),
        sa.ForeignKeyConstraint(("warehouse_id",), ["warehouse.id"]),
    )


def downgrade() -> None:
    op.drop_table("warehouse_product")
