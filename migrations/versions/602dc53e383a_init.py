"""Init

Revision ID: 602dc53e383a
Revises: bedb471f28cd
Create Date: 2023-03-13 16:16:20.633203

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '602dc53e383a'
down_revision = 'bedb471f28cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jeans', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=mysql.INTEGER(),
               type_=sa.Float(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jeans', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(),
               type_=mysql.INTEGER(),
               existing_nullable=True)

    # ### end Alembic commands ###
