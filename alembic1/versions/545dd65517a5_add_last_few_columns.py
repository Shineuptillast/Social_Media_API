"""Add last few columns

Revision ID: 545dd65517a5
Revises: b6c0c84acc30
Create Date: 2023-03-09 05:52:01.365765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '545dd65517a5'
down_revision = 'b6c0c84acc30'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')))


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
