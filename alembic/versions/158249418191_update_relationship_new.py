"""update relationship new

Revision ID: 158249418191
Revises: 28d883d04dd2
Create Date: 2025-05-26 12:54:34.914717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '158249418191'
down_revision: Union[str, None] = '28d883d04dd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
