"""add content column to table

Revision ID: 7c82e0c08d4a
Revises: 93457cc73f92
Create Date: 2023-03-09 05:19:52.134569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c82e0c08d4a'
down_revision = '93457cc73f92'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
