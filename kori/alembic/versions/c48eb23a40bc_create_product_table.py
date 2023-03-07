"""create product table

Revision ID: c48eb23a40bc
Revises: 2929c8b40852
Create Date: 2023-02-12 20:09:40.300571

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = "c48eb23a40bc"
down_revision = "2929c8b40852"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "product",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("org_id", UUID(as_uuid=True), nullable=False),
        sa.Column("reorder_level", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(("org_id",), ["organization.id"]),
    )


def downgrade() -> None:
    op.drop_table("product")
