"""create global_config table

Revision ID: 8588dd347b82
Revises: 5a6955661060
Create Date: 2023-02-12 20:02:45.242999

"""
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = '8588dd347b82'
down_revision = '5a6955661060'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "global_config",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("org_id", UUID(as_uuid=True), nullable=False),
        sa.Column("config_type", sa.String(255), nullable=False),
        sa.Column("value", sa.String(255), nullable=False),
        sa.ForeignKeyConstraint(("org_id",), ["organisation.id"]),
    )


def downgrade() -> None:
    op.drop_table("global_config")
