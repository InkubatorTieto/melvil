"""create books table

Revision ID: cb0416ee0cbc
Revises:
Create Date: 2018-05-09 14:37:25.484216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb0416ee0cbc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'books',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('author', sa.Unicode(200), nullable=False),
    )


def downgrade():
    op.drop_table('books')
