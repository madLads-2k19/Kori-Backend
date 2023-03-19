"""default_store_in_user

Revision ID: 33f133688a49
Revises: f4a2be1b7417
Create Date: 2023-03-19 12:10:57.254448

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import UUID

# revision identifiers, used by Alembic.
revision = "33f133688a49"
down_revision = "f4a2be1b7417"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("user") as batch_op:
        batch_op.add_column(sa.Column("default_store_id", UUID(as_uuid=True), nullable=True))
        batch_op.create_foreign_key("fk_user_store", "store", ["default_store_id"], ["id"])


def downgrade() -> None:
    with op.batch_alter_table("user") as batch_op:
        batch_op.drop_constraint("fk_user_store")
        batch_op.drop_column("default_store_id")
