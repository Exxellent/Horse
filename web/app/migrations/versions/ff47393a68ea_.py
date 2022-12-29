"""empty message

Revision ID: ff47393a68ea
Revises: 
Create Date: 2022-12-23 20:39:31.778252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff47393a68ea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('horses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hz', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('horses', schema=None) as batch_op:
        batch_op.drop_column('hz')

    # ### end Alembic commands ###