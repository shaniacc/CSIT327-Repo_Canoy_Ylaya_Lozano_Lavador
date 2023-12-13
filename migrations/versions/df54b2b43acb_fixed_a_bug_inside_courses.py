"""fixed a bug inside courses

Revision ID: df54b2b43acb
Revises: adc7ac108e08
Create Date: 2023-12-14 02:07:37.162404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df54b2b43acb'
down_revision = 'adc7ac108e08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.drop_index('course_code')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.create_index('course_code', ['course_code'], unique=False)

    # ### end Alembic commands ###
