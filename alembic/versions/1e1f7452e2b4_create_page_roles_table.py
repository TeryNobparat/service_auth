"""Create page_roles table

Revision ID: 1e1f7452e2b4
Revises: 74c5c9fdb7af
Create Date: 2025-05-28 14:02:19.313562

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e1f7452e2b4'
down_revision: Union[str, None] = '74c5c9fdb7af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
