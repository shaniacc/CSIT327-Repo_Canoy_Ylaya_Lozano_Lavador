"""changed dt of faceImage

Revision ID: 15210e6a51bf
Revises: 40c94fdf79f0
Create Date: 2023-11-08 05:52:50.020360

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '15210e6a51bf'
down_revision = '40c94fdf79f0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('faceImage',
               existing_type=mysql.TEXT(),
               type_=sa.LargeBinary(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('student', schema=None) as batch_op:
        batch_op.alter_column('faceImage',
               existing_type=sa.LargeBinary(),
               type_=mysql.TEXT(),
               existing_nullable=False)

    # ### end Alembic commands ###
