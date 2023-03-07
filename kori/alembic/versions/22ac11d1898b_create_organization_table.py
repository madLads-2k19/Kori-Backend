"""create organization table

Revision ID: 22ac11d1898b
Revises:
Create Date: 2023-02-12 19:19:24.506504

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = "22ac11d1898b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "organization",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.String(128), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("organization")
