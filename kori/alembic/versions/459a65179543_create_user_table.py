"""create user table

Revision ID: 459a65179543
Revises: 22ac11d1898b
Create Date: 2023-02-12 19:39:44.206378

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = "459a65179543"
down_revision = "22ac11d1898b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("org_id", UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(128), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("pass_hash", sa.LargeBinary(128), nullable=False),
        sa.Column("permission_level", sa.String(32), nullable=False),
        sa.ForeignKeyConstraint(("org_id",), ["organization.id"]),
    )


def downgrade() -> None:
    op.drop_table("user")
