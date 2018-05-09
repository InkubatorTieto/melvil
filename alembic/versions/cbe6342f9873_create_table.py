"""create table
Revision ID: cbe6342f9873
Revises: 
Create Date: 2018-05-09 15:13:03.857397

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cbe6342f9873'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(80), unique=True, nullable=False),
        sa.Column('email', sa.Unicode(200)),
    )


def downgrade():
    op.drop_table('account')
