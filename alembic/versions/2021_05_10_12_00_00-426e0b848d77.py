"""Add BlogPost.members_only

Revision ID: 426e0b848d77
Revises: 73c9d707134b
Create Date: 2021-05-10 12:00:00

"""

# revision identifiers, used by Alembic.
revision = '426e0b848d77'
down_revision = '73c9d707134b'

from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    op.add_column('blog', sa.Column('members_only', sa.Boolean(), nullable=True, default=False))
    op.create_index(op.f('ix_blog_members_only'), 'blog', ['members_only'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_blog_members_only'), table_name='blog')
    op.drop_column('blog', 'members_only')
