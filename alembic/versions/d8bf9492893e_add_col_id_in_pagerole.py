"""add col id in PageRole

Revision ID: d8bf9492893e
Revises: 158249418191
Create Date: 2025-05-28 13:53:03.467597

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd8bf9492893e'
down_revision: Union[str, None] = '158249418191'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
