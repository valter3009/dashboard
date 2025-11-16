"""Add is_default column to boards

Revision ID: b12c3d4e5f6g
Revises: a00e8f71a73b
Create Date: 2025-11-16 12:00:00.000000+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b12c3d4e5f6g'
down_revision = 'a00e8f71a73b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add is_default column to boards table
    op.add_column('boards', sa.Column('is_default', sa.Integer(), server_default='0', nullable=True))


def downgrade() -> None:
    # Remove is_default column from boards table
    op.drop_column('boards', 'is_default')
