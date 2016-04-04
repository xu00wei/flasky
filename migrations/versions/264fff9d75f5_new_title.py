"""new title

Revision ID: 264fff9d75f5
Revises: eae2a5f9bda
Create Date: 2016-04-01 22:06:28.137599

"""

# revision identifiers, used by Alembic.
revision = '264fff9d75f5'
down_revision = 'eae2a5f9bda'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('title', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'title')
    ### end Alembic commands ###
