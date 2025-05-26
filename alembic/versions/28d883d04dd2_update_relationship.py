"""update relationship

Revision ID: 28d883d04dd2
Revises: 9a9ffca29572
Create Date: 2025-05-26 12:00:03.766444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28d883d04dd2'
down_revision: Union[str, None] = '9a9ffca29572'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
