"""add redundant colum

Revision ID: c4247fdc7153
Revises: cbe6342f9873
Create Date: 2018-05-09 16:16:24.804608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4247fdc7153'
down_revision = 'cbe6342f9873'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('redundant column', sa.Column('super_column', sa.DateTime))


def downgrade():
    op.drop_column('redundant_column', 'super_column')
