"""Create reorder_placed column


Revision ID: d367b143516b
Revises: 33f133688a49
Create Date: 2023-03-20 18:58:52.028516

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "d367b143516b"
down_revision = "33f133688a49"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("store_product") as batch_op:
        batch_op.add_column(sa.Column("reorder_placed", sa.Boolean(), default=False))


def downgrade() -> None:
    with op.batch_alter_table("store_product") as batch_op:
        batch_op.drop_column("reorder_placed")
