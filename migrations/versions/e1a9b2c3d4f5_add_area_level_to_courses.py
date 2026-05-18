"""add area and level to courses

Revision ID: e1a9b2c3d4f5
Revises: d9c1a7e6f2ab
Create Date: 2026-05-18 17:33:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1a9b2c3d4f5'
down_revision: Union[str, Sequence[str], None] = 'd9c1a7e6f2ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('courses', sa.Column('area', sa.String(), nullable=True))
    op.add_column('courses', sa.Column('level', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('courses', 'level')
    op.drop_column('courses', 'area')
