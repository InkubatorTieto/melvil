"""test migration

Revision ID: 4d415bf6ccf7
Revises: fcf5b40b6245
Create Date: 2018-05-11 10:59:21.951432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d415bf6ccf7'
down_revision = 'fcf5b40b6245'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'articles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('author', sa.Unicode(200), nullable=False),
    )


def downgrade():
    op.drop_table('articles')
