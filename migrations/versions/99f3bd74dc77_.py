"""empty message

Revision ID: 99f3bd74dc77
Revises: 
Create Date: 2021-04-30 21:53:48.874233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99f3bd74dc77'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('songs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('link', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('songs')
    # ### end Alembic commands ###
