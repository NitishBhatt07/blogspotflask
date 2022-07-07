"""Rename AddPost table to Posts

Revision ID: 07ba75819e51
Revises: d5b2bb26354b
Create Date: 2022-07-04 22:56:30.828767

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '07ba75819e51'
down_revision = 'd5b2bb26354b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('add_post', schema=None) as batch_op:
        batch_op.drop_index('id')

    op.drop_table('add_post')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('add_post',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('title', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('content', mysql.VARCHAR(length=1000), nullable=False),
    sa.Column('author', mysql.VARCHAR(length=250), nullable=False),
    sa.Column('posted_on', mysql.DATETIME(), nullable=True),
    sa.Column('post_pic', mysql.VARCHAR(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    with op.batch_alter_table('add_post', schema=None) as batch_op:
        batch_op.create_index('id', ['id'], unique=False)

    # ### end Alembic commands ###