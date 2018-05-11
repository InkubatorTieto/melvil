"""test

Revision ID: fcf5b40b6245
Revises: cb0416ee0cbc
Create Date: 2018-05-10 11:43:31.506581

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fcf5b40b6245'
down_revision = 'cb0416ee0cbc'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        'book',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('author', sa.Unicode(200), nullable=False),
    )


def downgrade():
    op.drop_table('books')
