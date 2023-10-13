"""add task isCompleted column

Revision ID: b8b8005d81a5
Revises: a91a6b96286b
Create Date: 2023-10-13 22:48:43.807716

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8b8005d81a5'
down_revision = 'a91a6b96286b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('isCompleted', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('isCompleted')

    # ### end Alembic commands ###
