"""empty message

Revision ID: c3ed22289a5b
Revises: 
Create Date: 2018-03-08 23:42:33.706796

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3ed22289a5b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('similar', sa.Column('similarids', sa.String(), nullable=True))
    op.drop_column('similar', 'simlarids')
    op.add_column('title_full', sa.Column('netflixid', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('title_full', 'netflixid')
    op.add_column('similar', sa.Column('simlarids', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('similar', 'similarids')
    # ### end Alembic commands ###
