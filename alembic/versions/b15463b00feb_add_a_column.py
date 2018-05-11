"""add a column

Revision ID: b15463b00feb
Revises: 50ad2794d56c
Create Date: 2018-05-09 14:08:04.615338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b15463b00feb'
down_revision = '50ad2794d56c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))


def downgrade():
    op.drop_column('account', 'last_transaction_date')
