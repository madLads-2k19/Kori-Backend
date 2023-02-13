"""create store table

Revision ID: 910e53bb67cc
Revises: 459a65179543
Create Date: 2023-02-12 19:48:47.550996

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = '910e53bb67cc'
down_revision = '459a65179543'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "store",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("org_id", UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.ForeignKeyConstraint(("org_id",), ["organization.id"]),
    )


def downgrade() -> None:
    op.drop_table("store")
