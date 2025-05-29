"""Create page_roles table manually

Revision ID: 1b42adad7aae
Revises: 1e1f7452e2b4
Create Date: 2025-05-28 14:07:43.248607

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid

# เพิ่มตัวแปร revision และ down_revision
revision = '1b42adad7aae'
down_revision = '74c5c9fdb7af'  # ใส่ revision ID ของ migration ก่อนหน้า
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'page_roles',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column('page_id', UUID(as_uuid=True), sa.ForeignKey('pages.id'), nullable=False),
        sa.Column('role_id', UUID(as_uuid=True), sa.ForeignKey('roles.id'), nullable=False)
    )

def downgrade():
    op.drop_table('page_roles')

