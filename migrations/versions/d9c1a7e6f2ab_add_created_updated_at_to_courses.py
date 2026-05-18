"""add created_at and updated_at to courses

Revision ID: d9c1a7e6f2ab
Revises: c7c5f2a1b4d1
Create Date: 2026-05-18 17:14:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9c1a7e6f2ab'
down_revision: Union[str, Sequence[str], None] = 'c7c5f2a1b4d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'courses',
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        'courses',
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True)
    )

    op.execute("UPDATE courses SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
    op.execute("UPDATE courses SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL")

    op.alter_column('courses', 'created_at', nullable=False)
    op.alter_column('courses', 'updated_at', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('courses', 'updated_at')
    op.drop_column('courses', 'created_at')
