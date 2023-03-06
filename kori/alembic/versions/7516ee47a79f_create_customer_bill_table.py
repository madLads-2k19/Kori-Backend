"""create customer_bill table

Revision ID: 7516ee47a79f
Revises: de4af1b594b0
Create Date: 2023-02-12 20:58:29.325021

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = '7516ee47a79f'
down_revision = 'de4af1b594b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "customer_bill",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("org_id", UUID(as_uuid=True), nullable=False),
        sa.Column("store_id", UUID(as_uuid=True), nullable=False),
        sa.Column("customer_id", UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), nullable=False),
        sa.Column("payment_method", sa.String(64), nullable=False),
        sa.Column("products_total", sa.Numeric(2), nullable=False),
        sa.Column("discount_price", sa.Numeric(2), nullable=False),
        sa.Column("delivery_address", sa.Text(), nullable=True),
        sa.Column("delivery_charge", sa.Numeric(2), nullable=True),
        sa.Column("net_price", sa.Numeric(2), nullable=False),
        sa.Column("billed_at", sa.types.TIMESTAMP, nullable=False),
        sa.ForeignKeyConstraint(("org_id",), ["organization.id"]),
        sa.ForeignKeyConstraint(("store_id",), ["store.id"]),
        sa.ForeignKeyConstraint(("user_id",), ["user.id"]),
    )


def downgrade() -> None:
    op.drop_table("customer_bill")
