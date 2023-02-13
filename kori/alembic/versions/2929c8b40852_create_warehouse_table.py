"""create warehouse table

Revision ID: 2929c8b40852
Revises: 8588dd347b82
Create Date: 2023-02-12 20:06:19.908338

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = '2929c8b40852'
down_revision = '8588dd347b82'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "warehouse",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("org_id", UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.ForeignKeyConstraint(("org_id",), ["organisation.id"]),
    )


def downgrade() -> None:
    op.drop_table("warehouse")
