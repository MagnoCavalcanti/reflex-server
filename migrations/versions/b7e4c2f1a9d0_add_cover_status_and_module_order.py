"""add cover/status on courses and order on modules

Revision ID: b7e4c2f1a9d0
Revises: e1a9b2c3d4f5
Create Date: 2026-06-08 03:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7e4c2f1a9d0'
down_revision: Union[str, Sequence[str], None] = 'e1a9b2c3d4f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('courses', sa.Column('cover_image_url', sa.String(), nullable=True))
    op.add_column('courses', sa.Column('status', sa.String(), nullable=True))
    op.execute("UPDATE courses SET status = 'rascunho' WHERE status IS NULL")
    op.alter_column('courses', 'status', nullable=False)
    op.create_check_constraint(
        'chk_course_status_values',
        'courses',
        "status IN ('rascunho', 'publicado')"
    )

    op.add_column('modules', sa.Column('order_index', sa.Integer(), nullable=True))
    op.execute(
        """
        WITH ordered_modules AS (
            SELECT id, ROW_NUMBER() OVER (PARTITION BY course_id ORDER BY id) AS row_num
            FROM modules
        )
        UPDATE modules
        SET order_index = ordered_modules.row_num
        FROM ordered_modules
        WHERE modules.id = ordered_modules.id
        """
    )
    op.alter_column('modules', 'order_index', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('modules', 'order_index')
    op.drop_constraint('chk_course_status_values', 'courses', type_='check')
    op.drop_column('courses', 'status')
    op.drop_column('courses', 'cover_image_url')
