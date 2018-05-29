"""users table created

Revision ID: 63f3099ace00
Revises: 3f49e5c89b0b
Create Date: 2018-05-11 10:40:53.915209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63f3099ace00'
down_revision = '3f49e5c89b0b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'User',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, index=True, unique=True),
        sa.Column('email', sa.String, index=True, unique=True),
        sa.Column('password_hash', sa.String)
    )


def downgrade():
    op.drop_table('User')
