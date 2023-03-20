"""Create reorders table

Revision ID: 737b22dc5091
Revises: d367b143516b
Create Date: 2023-03-20 19:37:53.252900

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy import UUID, Boolean

# revision identifiers, used by Alembic.
revision = "737b22dc5091"
down_revision = "d367b143516b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "reorder",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("org_id", UUID(as_uuid=True), nullable=False),
        sa.Column("store_id", UUID(as_uuid=True), nullable=False),
        sa.Column("product_id", UUID(as_uuid=True), nullable=False),
        sa.Column("reorder_quantity", sa.Numeric(10, 3), nullable=False),
        sa.Column("reorder_time", sa.types.TIMESTAMP, nullable=False),
        sa.Column("supplier_paid", Boolean, default=False),
        sa.ForeignKeyConstraint(("org_id",), ["organization.id"]),
        sa.ForeignKeyConstraint(("product_id",), ["product.id"]),
        sa.ForeignKeyConstraint(("store_id",), ["store.id"]),
    )


def downgrade() -> None:
    op.drop_table("reorder")
