"""Add ckan_info to mods

Revision ID: 26f3fd0405c
Revises: 35597d56e8d
Create Date: 2015-01-18 17:00:28.941948

"""

# revision identifiers, used by Alembic.
revision = '26f3fd0405c'
down_revision = '35597d56e8d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mod', sa.Column('ckan_name', sa.String(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mod', 'ckan_name')
    ### end Alembic commands ###
