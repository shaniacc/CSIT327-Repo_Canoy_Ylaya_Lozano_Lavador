"""changed time slot to start_time & end_time

Revision ID: 5636fa4961c6
Revises: 15210e6a51bf
Create Date: 2023-11-10 00:51:45.585016

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5636fa4961c6'
down_revision = '15210e6a51bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('start_time', sa.Time(), nullable=False))
        batch_op.add_column(sa.Column('end_time', sa.Time(), nullable=False))
        batch_op.drop_column('time_slot')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time_slot', mysql.VARCHAR(length=50), nullable=False))
        batch_op.drop_column('end_time')
        batch_op.drop_column('start_time')

    # ### end Alembic commands ###
