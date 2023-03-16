"""create product_billed table

Revision ID: f4a2be1b7417
Revises: 7516ee47a79f
Create Date: 2023-02-12 21:12:13.433017

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = "f4a2be1b7417"
down_revision = "7516ee47a79f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product_billed",
        sa.Column("product_id", UUID(as_uuid=True), primary_key=True),
        sa.Column("version_id", sa.Integer(), primary_key=True),
        sa.Column("customer_bill_id", UUID(as_uuid=True), primary_key=True),
        sa.Column("product_quantity", sa.Numeric(10, 3), nullable=False),
        sa.Column("total_cost", sa.Numeric(10, 3), nullable=False),
        sa.ForeignKeyConstraint(
            ("product_id", "version_id"),
            ["product_version.product_id", "product_version.version_id"],
        ),
        sa.ForeignKeyConstraint(("customer_bill_id",), ["customer_bill.id"]),
    )


def downgrade() -> None:
    op.drop_table("product_billed")
