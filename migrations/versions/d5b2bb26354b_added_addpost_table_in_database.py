"""added AddPost table in database

Revision ID: d5b2bb26354b
Revises: 67e58e02ec0d
Create Date: 2022-07-03 09:08:11.884769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5b2bb26354b'
down_revision = '67e58e02ec0d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('add_post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_pic', sa.String(length=500), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('add_post', schema=None) as batch_op:
        batch_op.drop_column('post_pic')

    # ### end Alembic commands ###
