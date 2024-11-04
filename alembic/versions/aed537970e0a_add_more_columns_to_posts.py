"""add more columns to posts

Revision ID: aed537970e0a
Revises: fd472fa77d04
Create Date: 2024-11-04 11:42:15.353813

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = 'aed537970e0a'
down_revision: Union[str, None] = 'fd472fa77d04'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts',sa.Column('is_published', sa.Boolean(), nullable=False))
    op.add_column('posts',sa.Column('created_at', sa.DateTime(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False))
    


def downgrade() :
    op.drop_column('posts','is_publsihed')
    op.drop_column('posts','created_at')
    pass
