"""create customer table

Revision ID: 5a6955661060
Revises: 910e53bb67cc
Create Date: 2023-02-12 19:51:02.708754

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = '5a6955661060'
down_revision = '910e53bb67cc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "customer",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("org_id", UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone_number", sa.String(32), nullable=False),
        sa.Column("is_member", sa.Boolean(), default=False),
        sa.Column("membership_points", sa.Integer(), default=0),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("preferred_payment_method", sa.String(255), nullable=True),
        sa.ForeignKeyConstraint(("org_id",), ["organisation.id"]),
    )


def downgrade() -> None:
    op.drop_table("customer")
