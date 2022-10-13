"""empty message

Revision ID: 7fcd34442367
Revises: 
Create Date: 2022-10-13 16:22:11.690678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fcd34442367'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recipe', sa.Column('key', sa.Boolean(), nullable=True))
    op.alter_column('recipe', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('recipe', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    op.drop_column('recipe', 'key')
    # ### end Alembic commands ###